import uuid
from fastapi import Depends, HTTPException, Request, status
from fastapi.responses import JSONResponse
from app import create_app
from sqlalchemy.orm import Session
from models.suite import Suite
from db import get_session, init_db
from suites import suites, SuitesOptions
from models.scan import ScanRequest, Scan
from models.task import Task
from tasks import run_prompt, celery_app
from celery.result import AsyncResult
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

init_db()
app = create_app()
limiter = Limiter(key_func=get_remote_address) # create rate limit to a specific user

@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={"message": "Too many requests, slow down!"}
    )

@app.post("/scan")
@limiter.limit("5/minute") # user can make 5 requests per minute
def create_scan(request: Request, scan: ScanRequest, session: Session = Depends(get_session)):
    scan_id: str = str(uuid.uuid4())
    try:
        prompts: list[str] = suites.get(SuitesOptions(scan.suite), None)
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Suite not found")

    db_scan = Scan(id=scan_id, url=scan.url)
    session.add(db_scan)

    for prompt in prompts:
        # create async task for each prompt 
        celery_task = run_prompt.delay(scan.url, prompt)
        db_task = Task(id=celery_task.id, prompt=prompt, isCompleted=False, scan=db_scan)
        session.add(db_task)
    
    session.commit()
    return {"scanId": scan_id}

@app.get('/status/{scanId}')
def get_status(scanId: str, session: Session = Depends(get_session)):
    scan = session.query(Scan).filter(Scan.id == scanId).first()
    if not scan:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ScanId not found")
    
    total_tasks: int = len(scan.tasks)
    completed_tasks: int = 0

    for task in scan.tasks:
        db_task = session.query(Task).filter(Task.id == task.id).first()
        task_status = AsyncResult(task.id, app=celery_app) 
        if task_status.ready():
            completed_tasks+=1
            db_task.isCompleted = True
            session.commit()
    
    return {"completed": f"{((completed_tasks / total_tasks) * 100):.2f}%"} # calculate how many tasks are completed

@app.get('/results/{scanId}')
def get_results(scanId: str, session: Session = Depends(get_session)):
    scan = session.query(Scan).filter(Scan.id == scanId).first()
    if not scan:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ScanId not found")
    
    results: list = []
    for task in scan.tasks:
        task_status = AsyncResult(task.id, app=celery_app)
        if task_status.ready():
            # get only the latest prompt run response
            last_response = task_status.result['response']['agent_activity'][-1]['response']
            results.append({"prompt": task.prompt, "response": last_response, "status": "Finished"})
        else:
            results.append({"prompt": task.prompt, "status": "prompt still running..."})

    return {"ScanId": scanId, "results": results}

@app.get('/suites')
def get_all_suites(session: Session = Depends(get_session)):
    suites = session.query(Suite).all()
    return [suite.name for suite in suites]

@app.get('/scans')
def get_all_scans(session: Session = Depends(get_session)):
    scans = session.query(Scan).all()
    result = []

    for scan in scans:
        db_task = session.query(Task).filter(Task.scan_id == scan.id).first()
        result.append({
            "id": scan.id,
            "url": scan.url,
            "completed": db_task.isCompleted
        })
    
    return result

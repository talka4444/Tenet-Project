import uuid
from fastapi import Depends, HTTPException, status
from app import create_app
from sqlalchemy.orm import Session
from models.suite import Suite
from db import get_session, init_db
from suites import suites, SuitesOptions
from models.scan import ScanRequest, Scan
from models.task import Task
from tasks import run_prompt, celery_app
from celery.result import AsyncResult

init_db()
app = create_app()

@app.post("/scan")
def create_scan(scan: ScanRequest, session: Session = Depends(get_session)):
    scan_id: str = str(uuid.uuid4())
    try:
        prompts: list[str] = suites.get(SuitesOptions(scan.suite), None)
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Suite not found")

    db_scan = Scan(id=scan_id, url=scan.url)
    session.add(db_scan)

    for prompt in prompts:
        celery_task = run_prompt.delay(scan.url, prompt)
        db_task = Task(id=celery_task.id, prompt=prompt, scan=db_scan)
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
        task_status = AsyncResult(task.id, app=celery_app) 
        if task_status.ready():
            completed_tasks+=1

    
    return {"completed": f"{((completed_tasks / total_tasks) * 100):.2f}%"}

@app.get('/results/{scanId}')
def get_results(scanId: str, session: Session = Depends(get_session)):
    scan = session.query(Scan).filter(Scan.id == scanId).first()
    if not scan:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ScanId not found")
    
    results: list = []
    for task in scan.tasks:
        task_status = AsyncResult(task.id, app=celery_app)
        if task_status.ready():
            print(task_status.result)
            last_response = task_status.result['response']['agent_activity'][-1]['response']
            results.append({"prompt": task.prompt, "response": last_response, "status": "Finished"})
        else:
            results.append({"prompt": task.prompt, "status": "prompt still running..."})

    return {"ScanId": scanId, "results": results}

@app.get('/suites')
def get_all_suites(session: Session = Depends(get_session)):
    suites = session.query(Suite).all()
    return [suite.name for suite in suites]

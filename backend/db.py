from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from suites import suites
import os

engine = create_engine(os.getenv("DATABASE_URL", "sqlite:///./tenet.db"), connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def init_db():
    from models.prompt import Prompt
    from models.suite import Suite

    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    # we add all the suites and prompts to the DB if doesn't already exists
    try:
        for suite_enum, prompt_list in suites.items():
            suite_obj = db.query(Suite).filter_by(name=suite_enum.value).first()
            if not suite_obj:
                suite_obj = Suite(name=suite_enum.value)
                db.add(suite_obj)
                db.flush() 

            for prompt_text in prompt_list:
                exists = db.query(Prompt).filter_by(text=prompt_text, suite_id=suite_obj.id).first()
                if not exists:
                    db.add(Prompt(text=prompt_text, suite_id=suite_obj.id))
        db.commit()
    finally:
        db.close()

def get_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
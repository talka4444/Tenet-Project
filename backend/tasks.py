from celery import Celery
from faker import Faker
from fastapi import HTTPException, status
import requests

fake = Faker()

celery_app = Celery(
    "tasks",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0",
)

@celery_app.task
def run_prompt(chat_url: str, prompt: str):
    payload = {
        "name": fake.first_name(),
        "email": fake.email(),
        "message": prompt,
        "terms_accepted": True,
        "marketing_opt_in": True,
        "chat_history": [],
        "session_id": ""
    }

    try:
        bot_response = requests.post(chat_url, json=payload)
        bot_response.raise_for_status()
        response = bot_response.json()

    except Exception as e:
        response = {"error": str(e)}
    
    return {
        "prompt": prompt,
        "response": response
    }

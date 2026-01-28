from fastapi import APIRouter
from schemas.email_schema import EmailInput
from schemas.response_schema import EmailResponse
from app.core.pipeline import process_email

router = APIRouter()

@router.post("/classify", response_model=EmailResponse)
def classify_email(payload: EmailInput):
    return process_email(payload.text)

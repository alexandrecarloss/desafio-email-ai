from pydantic import BaseModel

class EmailResponse(BaseModel):
    intent: str
    stage: str
    action: str
    suggested_reply: str

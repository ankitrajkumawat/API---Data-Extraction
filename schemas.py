# app/models/schemas.py

from pydantic import BaseModel


# Schema for /process_url endpoint
class ProcessURLRequest(BaseModel):
    url: str


# Schema for /process_pdf endpoint
class ProcessResponse(BaseModel):
    chat_id: str
    message: str


# Schema for /chat endpoint
class ChatRequest(BaseModel):
    chat_id: str
    question: str


# Schema for /chat response
class ChatResponse(BaseModel):
    response: str

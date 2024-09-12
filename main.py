import uuid

from models.schemas import ProcessResponse, ProcessURLRequest, ChatResponse, ChatRequest
from utils.scrapper import scrape_url
from utils.pdf_processor import extract_text_from_pdf
from database.storage import store_content, get_content_by_id
from utils.embeddings import find_relevant_response
from fastapi import FastAPI, HTTPException, UploadFile, File


app = FastAPI(title="Chat Backend Service")


@app.post("/process_url", response_model=ProcessResponse)
async def process_url(request: ProcessURLRequest):
    try:
        content = scrape_url(request.url)
        if not content:
            raise HTTPException(status_code=400,
                                detail="Failed to scrape content from the URL.")
        chat_id = str(uuid.uuid4())
        store_content(chat_id, content)
        return ProcessResponse(chat_id=chat_id,
                               message="URL content processed and stored successfully.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/process_pdf", response_model=ProcessResponse)
async def process_pdf(file: UploadFile = File(...)):
    try:
        if file.content_type != 'application/pdf':
            raise HTTPException(status_code=400,
                                detail="Invalid file type. Only PDF files are allowed.")
        content = await extract_text_from_pdf(file)
        if not content:
            raise HTTPException(status_code=400,
                                detail="Failed to extract text from the PDF.")
        chat_id = str(uuid.uuid4())
        store_content(chat_id, content)
        return ProcessResponse(chat_id=chat_id,
                               message="PDF content processed and stored successfully.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        content = get_content_by_id(request.chat_id)
        if not content:
            raise HTTPException(status_code=404,
                                detail="Content not found for the given chat_id.")
        response = find_relevant_response(request.question, content)
        return ChatResponse(response=response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

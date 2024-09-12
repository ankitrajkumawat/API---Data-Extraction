import io
from PyPDF2 import PdfReader


async def extract_text_from_pdf(file) -> str:
    reader = PdfReader(io.BytesIO(await file.read()))
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    cleaned_text = ' '.join(text.split())  # Removing extra whitespace and line breaks
    return cleaned_text

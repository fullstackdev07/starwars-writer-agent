from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.book_writer import generate_user_prompt_driven_book
from app.book_pdf_exporter import save_book_as_pdf
from dotenv import load_dotenv
import os

load_dotenv()
app = FastAPI()

class BookRequest(BaseModel):
    user_input: str

@app.post("/generate-book/")
async def generate_star_wars_book(data: BookRequest):
    user_prompt = data.user_input.strip()

    if not user_prompt:
        raise HTTPException(status_code=400, detail="Prompt cannot be empty.")

    # Generate long book
    book_text = generate_user_prompt_driven_book(user_prompt)

    # Save to PDF
    filename = f"{user_prompt[:30].replace(' ', '_')}.pdf"
    pdf_path = save_book_as_pdf("Your Star Wars Story", book_text, filename=filename)

    return {
        "title": "Your Star Wars Story",
        "prompt": user_prompt,
        "content_preview": book_text[:1500] + "...",
        "pdf_file": pdf_path
    }
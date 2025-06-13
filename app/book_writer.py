from openai import OpenAI
import os
import time

openai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
MODEL = "gpt-4-1106-preview"

def generate_chunk(prompt: str, tokens: int = 2048) -> str:
    response = openai.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.75,
        max_tokens=tokens
    )
    return response.choices[0].message.content.strip()

def generate_long_chapter(prompt: str, target_words=1500) -> str:
    full_text = ""
    current_word_count = 0
    retries = 0

    while current_word_count < target_words and retries < 5:
        chunk = generate_chunk(f"Continue writing the story: {prompt}")
        full_text += "\n" + chunk
        current_word_count = len(full_text.split())
        time.sleep(1)
        retries += 1

    return full_text.strip()

def generate_user_prompt_driven_book(user_prompt: str) -> str:
    book = []

    # Prologue
    book.append("## Prologue\n\n" + generate_long_chapter(f"Write a detailed prologue for a Star Wars book about: {user_prompt}", target_words=1500))

    # Chapters
    for i in range(25):
        chapter_title = f"Chapter {i+1}"
        print(f"Generating {chapter_title}...")
        chapter_prompt = f"{chapter_title}. Write a long, detailed story (~1500 words) for a Star Wars novel about: {user_prompt}"
        chapter_content = generate_long_chapter(chapter_prompt, target_words=1500)
        book.append(f"\n\n## {chapter_title}\n\n{chapter_content}")

    # Epilogue
    book.append("\n\n## Epilogue\n\n" + generate_long_chapter(f"Write a detailed epilogue for a Star Wars book about: {user_prompt}", target_words=1500))

    return "\n".join(book)
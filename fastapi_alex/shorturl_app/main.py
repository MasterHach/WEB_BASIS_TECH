from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, HttpUrl
import sqlite3
import random
import string

app = FastAPI()

DATABASE = "data/shortener.db"

class URL(BaseModel):
    original_url: HttpUrl

# Инициализация базы данных
def init_db():
    with sqlite3.connect(DATABASE) as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS urls (
            id INTEGER PRIMARY KEY,
            short_code TEXT UNIQUE NOT NULL,
            original_url TEXT NOT NULL,
            clicks INTEGER DEFAULT 0
        )
        """)

init_db()

def generate_short_code(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

@app.post("/shorten/")
def create_short_url(url: URL):
    """
    Сокращение ссылки до 6-ми символьного кода
    """
    short_code = generate_short_code()
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO urls (short_code, original_url) VALUES (?, ?)",
                       (short_code, str(url.original_url)))
        conn.commit()
        return {"short_url": f"http://localhost:8000/{short_code}"}

@app.get("/{short_code}")
def redirect_to_original(short_code: str):
    """
    Переадресация на оригинальную ссылку по вводу сокращенного кода ссылки
    """
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT original_url FROM urls WHERE short_code = ?", (short_code,))
        result = cursor.fetchone()
        if not result:
            raise HTTPException(status_code=404, detail="URL not found")
        
        cursor.execute(
            "UPDATE urls SET clicks = clicks + 1 WHERE short_code = ?", (short_code,)
        )

        conn.commit()

        return {"original_url": result[0]}
    
@app.get("/stats/{short_code}")
def get_url_stats(short_code: str):
    """
    Вывод информации о ссылке по коду ссылки
    """
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT original_url, clicks FROM urls WHERE short_code = ?", (short_code,)
        )
        result = cursor.fetchone()
        if not result:
            raise HTTPException(status_code=404, detail="Short URL not found")
        
        # Возвращаем статистику
        return {"short_id": short_code, "original_url": result[0], "clicks": result[1]}
    

@app.get("/top/{n}")
def get_top_links(n: int):
    """
    Вывод первых n самых популярных по просмотру ссылок
    """
    if n <= 0:
        raise HTTPException(status_code=400, detail="Parameter 'n' must be a positive integer")
    
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT short_code, original_url, clicks FROM urls ORDER BY clicks DESC LIMIT ?",
            (n,)
        )
        results = cursor.fetchall()

    return [
        {"short_code": row[0], "original_url": row[1], "clicks": row[2]}
        for row in results
    ]
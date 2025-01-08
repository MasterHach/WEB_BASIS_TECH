from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
import sqlite3

app = FastAPI()

DATABASE = "data/todo.db"

class Task(BaseModel):
    title: str
    description: str = None
    completed: bool = False

def init_db():
    with sqlite3.connect(DATABASE) as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            description TEXT,
            completed BOOLEAN NOT NULL
        )
        """)

init_db()

@app.post("/items")
def create_task(task: Task):
    """
    Создание задачи
    """
    with sqlite3.connect("data/todo.db") as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO tasks (title, description, completed) VALUES (?, ?, ?)",
                       (task.title, task.description, task.completed))
        conn.commit()
        return {"id": cursor.lastrowid, **task.dict()}

@app.get("/items")
def get_tasks():
    """
    Получение списка всех задач
    """
    with sqlite3.connect("data/todo.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tasks")
        tasks = cursor.fetchall()
        return tasks

@app.get("/items/{item_id}")
def get_task(item_id: int):
    """
    Получение задачи по ID
    """
    with sqlite3.connect("data/todo.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tasks WHERE id = ?", (item_id,))
        task = cursor.fetchone()
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        return task

@app.put("/items/{item_id}")
def update_task(item_id: int, task: Task):
    """
    Обновление задачи по ID
    """
    with sqlite3.connect("data/todo.db") as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE tasks SET title = ?, description = ?, completed = ? WHERE id = ?",
                       (task.title, task.description, task.completed, item_id))
        conn.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Task not found")
        return {"id": item_id, **task.dict()}

@app.delete("/items/{item_id}")
def delete_task(item_id: int):
    """
    Удаление задачи по ID
    """
    with sqlite3.connect("data/todo.db") as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tasks WHERE id = ?", (item_id,))
        conn.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Task not found")
        return {"detail": "Task deleted"}
    

@app.get("/tasks/search/")
def search_tasks(query: str = Query(..., min_length=1, description="Ключевое слово для поиска")):
    """
    Поиск задачи по названию или описанию
    """
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("""
        SELECT id, title, description, completed
        FROM tasks
        WHERE title LIKE ? OR description LIKE ?
        """, (f"%{query}%", f"%{query}%"))
        tasks = cursor.fetchall()

    if not tasks:
        raise HTTPException(status_code=404, detail="Задачи не найдены")
    
    return [
        {"id": row[0], "title": row[1], "description": row[2], "completed": bool(row[3])}
        for row in tasks
    ]
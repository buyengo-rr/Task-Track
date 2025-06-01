import sqlite3
from typing import List
import datetime
from model import Todo

conn = sqlite3.connect('todos.db')
c = conn.cursor()

def create_table():
    c.execute("""CREATE TABLE IF NOT EXISTS todos(
              task text,
              category text,
              date_added text,
              date_completed text,
              status integer,
              position integer)""")
    conn.commit()

create_table()

def insert_todo(todo: Todo):
    c.execute('SELECT count(*) FROM todos')
    count = c.fetchone()[0]
    todo.position = count if count else 0
    with conn:
        c.execute('INSERT INTO todos VALUES (?,?,?,?,?,?)',
                 (todo.task, todo.category, todo.date_added, todo.date_completed, todo.status, todo.position))
        conn.commit()

def get_all_todos() -> List[Todo]:
    c.execute('SELECT * FROM todos ORDER BY position')
    return [Todo(*row) for row in c.fetchall()]

def delete_todo(position):
    c.execute('SELECT count(*) FROM todos')
    count = c.fetchone()[0]
    with conn:
        c.execute("DELETE FROM todos WHERE position=?", (position,))
        for pos in range(position+1, count):
            change_position(pos, pos-1, False)
        conn.commit()

def change_position(old_position: int, new_position: int, commit=True):
    c.execute('UPDATE todos SET position = ? WHERE position = ?',
             (new_position, old_position))
    if commit:
        conn.commit()

def update_todo(position: int, task: str = None, category: str = None):
    with conn:
        if task and category:
            c.execute('UPDATE todos SET task = ?, category = ? WHERE position = ?',
                     (task, category, position))
        elif task:
            c.execute('UPDATE todos SET task = ? WHERE position = ?',
                     (task, position))
        elif category:
            c.execute('UPDATE todos SET category = ? WHERE position = ?',
                     (category, position))
        conn.commit()

def complete_todo(position: int):
    with conn:
        c.execute('UPDATE todos SET status = 2, date_completed = ? WHERE position = ?',
                 (datetime.datetime.now().isoformat(), position))
        conn.commit()
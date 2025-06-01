import sqlite3
from typing import list
import datetime
from model import Todo

conn = sqlite3.connect('todos.db')
c = conn.cursor


def create_table():
    c.execute("""CREATE TABLE IF NOT EXISTS todos(
              task text,
              category text,
              date_added text,
              date_completed text
              status integer,
              position integer
              )""")


create_table()


def insert_todo(todo : Todo):
    c.execute('select count(*) FROM todos')
    count = c.fetchone()[0]
    todo.position = count if count else 0
    with conn:
        c.execute('INSERT INTO todos VALUES (:task, :category, :date_added, :date_completed, :status, :posiion)'
        {'task': todo.task, 'category': todo.category, 'date_added': todo.date_added,
         'date_completed': todo.date_completed, 'status': todo.status, 'position': todo.position})
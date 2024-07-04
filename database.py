import psycopg2 as psql
import os
from dotenv import load_dotenv
load_dotenv()


class Database:
    @staticmethod
    async def connect(query: str, query_type: str):
        db = psql.connect(
            database=os.getenv("database"),
            user=os.getenv("user"),
            password=os.getenv("password"),
            port=os.getenv("port"),
            host=os.getenv("host"),
        )
        cursor = db.cursor()
        cursor.execute(query)
        data = ["insert", 'update', 'delete', 'alter', 'create']
        if query_type in data:
            db.commit()
            return "Changes data successfully"
        else:
            return cursor.fetchall()

    @staticmethod
    async def create_table():
        users = """
            CREATE TABLE IF NOT EXISTS users(
                id serial PRIMARY KEY,
                first_name VARCHAR(150),
                last_name VARCHAR(150),
                username VARCHAR(50),
                chat_id BIGINT,
                created_at TIMESTAMP DEFAULT now())"""

        await Database.connect(users, "create")

    @staticmethod
    async def check_user(user_id: int):
        query = f"SELECT * FROM users WHERE chat_id = {user_id}"
        user = await Database.connect(query, query_type="select")
        if len(user) == 0:
            return True
        else:
            return False


    @staticmethod
    async def save_user(data: dict):
        query = f"""INSERT INTO users (first_name, last_name, username, chat_id)
            VALUES ('{data['first_name']}', '{data['last_name']}', '{data['username']}', {data['chat_id']})"""
        await Database.connect(query, query_type="insert")




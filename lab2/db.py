import psycopg2
import os
import logging
from datetime import datetime, timedelta

class Database:
    def __init__(self):
        try:
            # Подключение к базе данных
            self.conn = psycopg2.connect(
                host=os.getenv("POSTGRES_HOST"),
                port=os.getenv("POSTGRES_PORT"),
                user=os.getenv("POSTGRES_USER"),
                password=os.getenv("POSTGRES_PASSWORD"),
                dbname=os.getenv("POSTGRES_DB")
            )
            self.cursor = self.conn.cursor()
            self.create_table()
        except psycopg2.OperationalError as e:
            logging.error(f"Error connecting to the database: {e}")
            raise

    def __del__(self):
        # Закрытие соединения с базой данных при удалении объекта
        if self.conn:
            self.cursor.close()
            self.conn.close()

    def create_table(self):
        """Создаём таблицу, если она не существует"""
        try:
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS logs (
                    id SERIAL PRIMARY KEY,
                    query TEXT NOT NULL,
                    response TEXT NOT NULL,
                    timestamp TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
                );
            """)
            self.conn.commit()
            logging.info("Table created successfully or already exists.")
        except Exception as e:
            logging.error(f"Error creating table: {e}")
    
    def log_to_db(self, query: str, response: str):
        """Записываем запрос и ответ в таблицу"""
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO logs (query, response, timestamp) VALUES (%s, %s, CURRENT_TIMESTAMP)",
                    (query, response)
                )
                self.conn.commit()
        except Exception as e:
            logging.error(f"Error logging to database: {e}")
    
    def get_all_logs(self):
        """Получаем все логи из базы данных"""
        try:
            self.cursor.execute("SELECT * FROM logs ORDER BY timestamp DESC;")
            logs = self.cursor.fetchall()
            return logs
        except Exception as e:
            logging.error(f"Error retrieving logs: {e}")
            return []

    def delete_logs_older_than(self, days: int):
        """Удаляем логи старше заданного количества дней"""
        try:
            cutoff_date = datetime.now() - timedelta(days=days)
            self.cursor.execute(
                "DELETE FROM logs WHERE timestamp < %s;", (cutoff_date,)
            )
            self.conn.commit()
            logging.info(f"Logs older than {days} days have been deleted.")
        except Exception as e:
            logging.error(f"Error deleting logs: {e}")

    def count_logs(self):
        """Возвращаем количество записей в таблице"""
        try:
            self.cursor.execute("SELECT COUNT(*) FROM logs;")
            count = self.cursor.fetchone()[0]
            return count
        except Exception as e:
            logging.error(f"Error counting logs: {e}")
            return 0

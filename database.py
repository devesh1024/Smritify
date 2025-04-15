import sqlite3
from typing import List, Tuple, Optional

class DatabaseManager:
    def __init__(self, db_name: str = 'smritify.db'):
        self.db_name = db_name
        self.conn = None
        self.cursor = None
        self.init_database()  # Initialize database when creating instance
    
    def init_database(self):
        """Initialize SQLite database and create necessary tables"""
        self.connect()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS questions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question TEXT NOT NULL,
                answer TEXT,
                subject TEXT,
                is_bookmarked INTEGER DEFAULT 0,
                is_understood INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.conn.commit()
        self.disconnect()
    
    def connect(self):
        """Establish connection to the database"""
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
    
    def disconnect(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
    
    def add_question(self, question: str, answer: str, subject: str) -> int:
        """Add a new question to the database"""
        self.connect()
        self.cursor.execute('''
            INSERT INTO questions (question, answer, subject)
            VALUES (?, ?, ?)
        ''', (question, answer, subject))
        question_id = self.cursor.lastrowid
        self.conn.commit()
        self.disconnect()
        return question_id
    
    def get_question(self, question_id: int) -> Optional[Tuple]:
        """Get a specific question by ID"""
        self.connect()
        self.cursor.execute('SELECT * FROM questions WHERE id = ?', (question_id,))
        question = self.cursor.fetchone()
        self.disconnect()
        return question
    
    def get_all_questions(self, subject: str = None) -> List[Tuple]:
        """Get all questions, optionally filtered by subject"""
        self.connect()
        if subject:
            self.cursor.execute('SELECT * FROM questions WHERE subject = ?', (subject,))
        else:
            self.cursor.execute('SELECT * FROM questions')
        questions = self.cursor.fetchall()
        self.disconnect()
        return questions
    
    def bookmark_question(self, question_id: int, bookmark: bool = True):
        """Bookmark or unbookmark a question"""
        self.connect()
        self.cursor.execute('''
            UPDATE questions
            SET is_bookmarked = ?
            WHERE id = ?
        ''', (1 if bookmark else 0, question_id))
        self.conn.commit()
        self.disconnect()
    
    def mark_as_understood(self, question_id: int):
        """Mark a question as understood"""
        self.connect()
        self.cursor.execute('''
            UPDATE questions
            SET is_understood = 1
            WHERE id = ?
        ''', (question_id,))
        self.conn.commit()
        self.disconnect()
    
    def get_bookmarked_questions(self) -> List[Tuple]:
        """Get all bookmarked questions"""
        self.connect()
        self.cursor.execute('SELECT * FROM questions WHERE is_bookmarked = 1')
        questions = self.cursor.fetchall()
        self.disconnect()
        return questions
    
    def get_unanswered_questions(self) -> List[Tuple]:
        """Get all questions without answers"""
        self.connect()
        self.cursor.execute('SELECT * FROM questions WHERE answer IS NULL')
        questions = self.cursor.fetchall()
        self.disconnect()
        return questions
    
    def update_answer(self, question_id: int, answer: str):
        """Update the answer for a specific question"""
        self.connect()
        self.cursor.execute('''
            UPDATE questions
            SET answer = ?
            WHERE id = ?
        ''', (answer, question_id))
        self.conn.commit()
        self.disconnect() 
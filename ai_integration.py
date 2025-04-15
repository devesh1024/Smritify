import os
from openai import OpenAI
from typing import Optional
from dotenv import load_dotenv

class AIAssistant:
    def __init__(self):
        load_dotenv()
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key or api_key == 'your_api_key_here':
            self.client = None
            print("Warning: OpenAI API key not set. AI features will be disabled.")
        else:
            self.client = OpenAI(api_key=api_key)
    
    def generate_answer(self, question: str) -> Optional[str]:
        """Generate an answer for a given question using ChatGPT"""
        if not self.client:
            return "AI features are disabled. Please set your OpenAI API key in the .env file."
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful study assistant. Provide concise and accurate answers to academic questions."},
                    {"role": "user", "content": question}
                ],
                max_tokens=150,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error generating answer: {e}")
            return None
    
    def suggest_questions(self, subject: str, topic: str) -> Optional[list]:
        """Generate relevant questions for a given subject and topic"""
        if not self.client:
            return ["AI features are disabled. Please set your OpenAI API key in the .env file."]
        
        try:
            prompt = f"Generate 5 important questions about {topic} in {subject}. Format each question on a new line."
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful study assistant. Generate relevant academic questions."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=200,
                temperature=0.7
            )
            questions = response.choices[0].message.content.split('\n')
            return [q.strip() for q in questions if q.strip()]
        except Exception as e:
            print(f"Error suggesting questions: {e}")
            return None 
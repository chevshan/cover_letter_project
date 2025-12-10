import os
import requests
from dotenv import load_dotenv

from groq import Groq

load_dotenv()

class CustomLLM:
    def __init__(self):
        self.api_key = f"{os.getenv('GROQ_API_KEY')}"
        self.model = "llama-3.3-70b-versatile"
    
    def invoke(self, prompt: str, system_prompt: str = None) -> str:
        messages = []

        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        messages.append({"role": "user", "content": prompt})

        try:
            client = Groq(api_key=self.api_key)

            response = client.chat.completions.create(
                messages=messages,
                model=self.model
            )
            content = response.choices[0].message.content
            return content
        
        except Exception as e:
            print(f"Error when calling LLM: {e}")
            return f"Error: {str(e)}"

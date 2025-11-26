import os
import requests
from dotenv import load_dotenv

load_dotenv()

class CustomLLM:
    def __init__(self):
        self.url = f"{os.getenv('IO_CHAT_URL')}"
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {os.getenv('BEARER_API_KEY')}" 
        }
        self.model = 'Qwen/Qwen3-235B-A22B-Thinking-2507'
    
    def load_prompt(self, file_path: str = "") -> str:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read().strip()
        except FileNotFoundError:
            print(f"File {file_path} is not found!")
            return ""
    
    def invoke(self, prompt: str, system_prompt: str = None) -> str:
        messages = []
        
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        messages.append({"role": "user", "content": prompt})
        
        data = {
            "model": self.model,
            "messages": messages
        }
        
        try:
            response = requests.post(self.url, headers=self.headers, json=data)
            response.raise_for_status()
            result = response.json()
            
            if 'choices' in result and len(result['choices']) > 0:
                content = result['choices'][0]['message']['content']
                if '</think>' in content:
                    return content.split('</think>')[1].strip()
                return content
            else:
                return "Error: couldn't get a responce from the model"
                
        except Exception as e:
            print(f"Error when calling LLM: {e}")
            return f"Error: {str(e)}"

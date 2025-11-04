import os
import requests
from pprint import pprint
from dotenv import load_dotenv

load_dotenv()

url = f"{os.getenv('IO_CHAT_URL')}"

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {os.getenv('BEARER_API_KEY')}" 
}

def load_prompt(file_path: str = "") -> str:
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read().strip()
    except FileNotFoundError:
        print(f"File {file_path} is not found!")
        return None

data = {
    "model": 'deepseek-ai/DeepSeek-R1-0528',
    "messages": [
        {
            "role": "system",
            "content": load_prompt(file_path="system_prompt.txt")
        },
        {
            "role": "user",
            "content": load_prompt(file_path="results/vacancy.txt")
        },
    ]
}

response = requests.post(url, headers=headers, json=data)
data = response.json()
pprint(data)

# text = data['choices'][0]['message']['content']
# print(text.split('</think>\n')[1])
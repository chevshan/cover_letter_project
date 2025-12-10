import os
import time
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


# load_prompt(file_path="system_prompt.txt")
data = {
    "model": 'Qwen/Qwen3-235B-A22B-Thinking-2507',
    "messages": [
        {
            "role": "system",
            "content": "You are a polite and kind interlocutor, respond to user requests without water, clearly and to the point."
        },
        {
            "role": "user",
            "content": "Hello, how are you?"
        },
    ]
}
start_time = time.time()
response = requests.post(url, headers=headers, json=data)
data = response.json()
print(f"Chat processed the request and gave the answer in {(time.time() - start_time):.2f}")
pprint(data)

# text = data['choices'][0]['message']['content']
# print(text.split('</think>\n')[1])
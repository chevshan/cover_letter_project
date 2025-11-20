import os
import requests
from pprint import pprint
from dotenv import load_dotenv

load_dotenv()

url = f"{os.getenv('IO_CHAT_MODELS')}"

headers = {"Authorization": f"Bearer {os.getenv('BEARER_API_KEY')}"}

response = requests.get(url, headers=headers)
data = response.json()
# pprint(data)

for i in range(len(data["data"])):
    name = data['data'][i]['id']
    print(name)
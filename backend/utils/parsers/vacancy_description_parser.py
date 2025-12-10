import requests
import json
from bs4 import BeautifulSoup
from typing import Optional
import os

def extract_vacancy_description(vacancy_id: str, save_to_file: Optional[str] = None) -> str:
    try:
        response = requests.get("https://api.hh.ru/vacancies/" + vacancy_id)
        response.raise_for_status()  
        
        data = response.content.decode('utf-8')
        parsed_json = json.loads(data)
        
        html_string = parsed_json.get('description', '')
        
        soup = BeautifulSoup(html_string, 'html.parser')
        description = soup.get_text().strip()
        
        if save_to_file:
            os.makedirs(os.path.dirname(save_to_file) if os.path.dirname(save_to_file) else '.', exist_ok=True)
            with open(save_to_file, 'w', encoding='utf-8') as f:
                f.write(description)
            print(f"Vacancy description saved in: {save_to_file}")
        
        return description
        
    except requests.exceptions.RequestException as e:
        raise Exception(f"Error when requesting vacancy {vacancy_id}: {e}")
    except json.JSONDecodeError as e:
        raise Exception(f"Error when parsing JSON: {e}")
    except KeyError:
        raise Exception("The key 'description' didn't found")
    finally:
        if 'response' in locals():
            response.close()
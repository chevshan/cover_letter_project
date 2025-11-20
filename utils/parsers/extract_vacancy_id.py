def extract_vacancy_id(url: str) -> str:
    try:
        base_url = url.split('?')[0]
        
        parts = base_url.rstrip('/').split('/')
        vacancy_id = parts[-1]
        
        if not vacancy_id.isdigit():
            raise ValueError(f"Invalid vacancy ID format: {vacancy_id}")
            
        return vacancy_id
        
    except Exception as e:
        raise ValueError(f"Failed to extract vacancy ID from URL: {url}") from e
def load_docs_from_txt(file_path: str) -> str:
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read().strip()
    except FileNotFoundError:
        print(f"File with document {file_path} doesn't found")
        return ""
    except Exception as e:
        print(f"Error reading the file with document: {e}")
        return ""
import os
from typing import Optional
from dotenv import load_dotenv
from llama_parse import LlamaParse

load_dotenv()

class PDFParser:
    
    def __init__(self, result_type: str = "markdown"): # text
        self.parser = self._setup_parser(result_type)
        self.result_type = result_type
    
    def _setup_parser(self, result_type: str) -> LlamaParse:
        api_key = os.getenv('LLAMA_API_KEY')

        if not api_key:
            raise ValueError("LLAMA_API_KEY not found in environment variables")
        
        return LlamaParse(api_key=api_key, result_type=result_type)
    
    def parse_pdf(self, file_path: str, save_to_file: Optional[str] = None) -> str:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"PDF file not found: {file_path}")
        
        extra_info = {"file_name": file_path}
        
        with open(file_path, "rb") as f:
            documents = self.parser.load_data(f, extra_info=extra_info)
        
        extracted_text = "\n".join(doc.text for doc in documents)

        if save_to_file:
            self._save_text_to_file(documents, save_to_file)
        
        return extracted_text
    
    def _save_text_to_file(self, text: str, file_path: str):
        with open(file_path, "w", encoding="utf-8") as f:
            for doc in text:
                f.write(doc.text)
        
        print(f"Text saved to: {file_path}")

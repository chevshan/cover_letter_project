import sys

from utils.parsers.pdf_parser import PDFParser
from utils.parsers.extract_vacancy_id import extract_vacancy_id
from utils.parsers.vacancy_description_parser import extract_vacancy_description

from langgraph_components.cover_letter_worflow import create_workflow
from langgraph_components.generate_cover_letter import generate_cover_letter

def main(vacancy_text: str, resume_text: str):
    try:
        workflow = create_workflow()
        
        print(f"Vacancy size: ({len(vacancy_text)} chars)")
        print(f"Resume size: ({len(resume_text)} chars)")
        
        print("Let's DOOOOO THIIIIS...")
        report = generate_cover_letter(vacancy_text, resume_text, workflow)
        
        output_file = "analysis_report_main_test.txt"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(report["cover_letter"])
        
        print(f"Analysis report saved in: {output_file}")
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":

    pdf_parser = PDFParser()

    vacancy_url = "https://hh.ru/vacancy/127825290?query=ML&hhtmFrom=vacancy_search_list"
    vacancy_id = extract_vacancy_id(vacancy_url)
    vacancy_text = extract_vacancy_description(vacancy_id, save_to_file="vacancy_description.txt")

    resume_text = pdf_parser.parse_pdf("docs/Test_CV.pdf", save_to_file="check_parser.txt")

    main(vacancy_text, resume_text)
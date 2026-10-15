import os
import pythoncom
from docx2pdf import convert

def convert_word_to_pdf(file_path: str) -> str:
    """
    Конвертує файл DOCX/DOC у PDF.
    Повертає шлях до згенерованого PDF-файлу.
    """
    pythoncom.CoInitialize()
    try:
        file_dir, file_name = os.path.split(file_path)
        file_base, _ = os.path.splitext(file_name)
        pdf_path = os.path.join(file_dir, f"{file_base}.pdf")

        try:
            convert(file_path, pdf_path)
        except Exception as e:
            # Якщо PDF фактично створився, ігноруємо помилку закрития Word
            if not (os.path.exists(pdf_path) and os.path.getsize(pdf_path) > 0):
                raise e

        return pdf_path
    finally:
        pythoncom.CoUninitialize()
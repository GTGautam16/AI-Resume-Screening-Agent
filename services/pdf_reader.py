from pathlib import Path
from pypdf import PdfReader

UPLOAD_FOLDER = Path("uploads")


def save_uploaded_file(uploaded_file):
    """
    Save uploaded PDF to uploads folder.
    """

    UPLOAD_FOLDER.mkdir(exist_ok=True)

    file_path = UPLOAD_FOLDER / uploaded_file.name

    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    return file_path

def extract_text_from_pdf(pdf_path):
    """
    Extract text from a PDF file.
    """

    reader = PdfReader(pdf_path)

    text = ""

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text
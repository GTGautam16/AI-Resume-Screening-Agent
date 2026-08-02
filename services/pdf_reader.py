from pathlib import Path
from pypdf import PdfReader
import re

UPLOAD_FOLDER = Path("uploads")


def save_uploaded_file(uploaded_file):
    """
    Save uploaded PDF to uploads folder.
    Works with both Streamlit and FastAPI uploads.
    """

    UPLOAD_FOLDER.mkdir(exist_ok=True)

    filename = getattr(uploaded_file, "name", None)

    if filename is None:
        filename = uploaded_file.filename

    file_path = UPLOAD_FOLDER / filename

    with open(file_path, "wb") as f:

        # Streamlit
        if hasattr(uploaded_file, "getbuffer"):
            f.write(uploaded_file.getbuffer())

        # FastAPI
        else:
            f.write(uploaded_file.file.read())

    return file_path

def extract_text_from_pdf(pdf_path):
    """
    Extract text from a PDF file.
    """

    try:
        reader = PdfReader(pdf_path)

        text = ""

        for page in reader.pages:
            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

        return text

    except Exception as e:
        raise Exception(f"Unable to read PDF: {e}")

def clean_text(text):
    """
    Clean extracted PDF text.
    """

    # Replace multiple spaces/tabs with a single space
    text = re.sub(r"[ \t]+", " ", text)

    # Replace 3 or more newlines with 2
    text = re.sub(r"\n{3,}", "\n\n", text)

    # Remove leading/trailing whitespace
    text = text.strip()

    return text
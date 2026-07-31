from pathlib import Path


UPLOAD_FOLDER = Path("uploads")


def save_uploaded_file(uploaded_file):
    """
    Save an uploaded PDF into the uploads folder.

    Parameters:
        uploaded_file: Streamlit UploadedFile object

    Returns:
        Path of the saved file
    """

    # Create uploads folder if it doesn't exist
    UPLOAD_FOLDER.mkdir(exist_ok=True)

    file_path = UPLOAD_FOLDER / uploaded_file.name

    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    return file_path
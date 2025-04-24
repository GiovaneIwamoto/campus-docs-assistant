import docx
import zipfile
import streamlit as st
from io import BytesIO
from typing import Union
from PyPDF2 import PdfReader

def extract_text_from_file(file: Union[BytesIO, st.runtime.uploaded_file_manager.UploadedFile], filetype: str) -> str:
    """
    Extract text content from a file based on its type.

    Args:
        file (Union[BytesIO, UploadedFile]): The uploaded file.
        filetype (str): File extension indicating the type (e.g., .pdf, .txt, .docx).
    """
        
    if filetype == ".pdf":
        reader = PdfReader(file)
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    
    elif filetype == ".txt":
        return file.getvalue().decode("utf-8")  

    elif filetype == ".docx":
        doc = docx.Document(file)
        return "\n".join([para.text for para in doc.paragraphs])

    else:
        raise ValueError(f"Unsupported file type: {filetype}")
    
def extract_files_from_zip(zip_files: BytesIO) -> list:
    """
    Extract supported files from a .zip archive and return them as (filename, file_content) tuples.

    Args:
        zip_files (BytesIO): The uploaded .zip file.
    Returns:
        List[Tuple[str, BytesIO]]: A list of (filename, BytesIO) tuples for supported files.
    """
    suported_exts = [".pdf", ".txt", ".docx"]
    extracted_files = []
    
    with zipfile.ZipFile(zip_files) as archive:
        for file_info in archive.infolist():
            filename = file_info.filename
            file_ext = f".{filename.split('.')[-1].lower()}"
            
            if file_ext in suported_exts and not file_info.is_dir():
                with archive.open(file_info) as file:
                    file_data = file.read()
                    extracted_files.append((filename, BytesIO(file_data)))
    
    return extracted_files
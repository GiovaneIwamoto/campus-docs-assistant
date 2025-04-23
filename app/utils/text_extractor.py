import docx
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
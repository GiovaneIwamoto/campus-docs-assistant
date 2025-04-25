import zipfile
from io import BytesIO

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
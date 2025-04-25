import zipfile
from io import BytesIO
from typing import List, Tuple

class FileExtractorError(Exception):
    """Custom exception for file extraction errors."""
    pass

def extract_files_from_zip(zip_files: BytesIO) -> List[Tuple[str, BytesIO]]:
    """
    Extract supported files from a .zip archive and return them as (filename, file_content) tuples.

    Args:
        zip_files (BytesIO): The uploaded .zip file.
    
    Returns:
        List[Tuple[str, BytesIO]]: A list of (filename, BytesIO) tuples for supported files.

    Raises:
        FileExtractorError: If the provided file is not a valid .zip archive or if no supported files are found.
    """
    supported_exts = [".pdf", ".txt", ".docx"]
    extracted_files = []

    try:
        # Attempt to open the zip file
        with zipfile.ZipFile(zip_files) as archive:
            for file_info in archive.infolist():
                filename = file_info.filename
                file_ext = f".{filename.split('.')[-1].lower()}"

                # Check if the file has a supported extension and is not a directory
                if file_ext in supported_exts and not file_info.is_dir():
                    try:
                        with archive.open(file_info) as file:
                            file_data = file.read()
                            extracted_files.append((filename, BytesIO(file_data)))
                    
                    except Exception as e:
                        raise FileExtractorError(f"Error reading file '{filename}' from the archive: {e}")
    
    except zipfile.BadZipFile:
        raise FileExtractorError("The provided file is not a valid .zip archive.")
    
    except Exception as e:
        raise FileExtractorError(f"An unexpected error occurred while extracting files: {e}")

    if not extracted_files:
        raise FileExtractorError("No supported files were found in the .zip archive.")

    return extracted_files
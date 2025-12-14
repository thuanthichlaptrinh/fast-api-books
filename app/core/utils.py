import os
import uuid
from pathlib import Path
from typing import Tuple
from fastapi import UploadFile, HTTPException, status


# Allowed image extensions
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp"}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB


def validate_image_file(file: UploadFile) -> None:
    """
    Validate uploaded image file
    
    Args:
        file: Uploaded file from FastAPI
        
    Raises:
        HTTPException: If file is invalid
    """
    # Check file extension
    file_ext = Path(file.filename).suffix.lower()
    if file_ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid file type. Allowed types: {', '.join(ALLOWED_EXTENSIONS)}"
        )
    
    # Check content type
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File must be an image"
        )


def generate_unique_filename(original_filename: str) -> str:
    """
    Generate unique filename using UUID
    
    Args:
        original_filename: Original filename from upload
        
    Returns:
        Unique filename with original extension
    """
    file_ext = Path(original_filename).suffix.lower()
    unique_name = f"{uuid.uuid4().hex}{file_ext}"
    return unique_name


async def save_upload_file(
    file: UploadFile, 
    save_dir: str = "app/static/covers"
) -> Tuple[str, str]:
    """
    Save uploaded file to disk
    
    Args:
        file: Uploaded file from FastAPI
        save_dir: Directory to save the file
        
    Returns:
        Tuple of (file_path, url_path)
        - file_path: Full path to saved file on disk
        - url_path: URL path to access the file (e.g., /static/covers/filename.jpg)
        
    Raises:
        HTTPException: If save fails
    """
    # Validate file
    validate_image_file(file)
    
    # Create directory if not exists
    Path(save_dir).mkdir(parents=True, exist_ok=True)
    
    # Generate unique filename
    unique_filename = generate_unique_filename(file.filename)
    file_path = os.path.join(save_dir, unique_filename)
    
    # Save file
    try:
        contents = await file.read()
        
        # Check file size
        if len(contents) > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"File size exceeds maximum allowed size of {MAX_FILE_SIZE / (1024*1024)}MB"
            )
        
        with open(file_path, "wb") as f:
            f.write(contents)
        
        # Generate URL path
        url_path = f"/static/covers/{unique_filename}"
        
        return file_path, url_path
        
    except Exception as e:
        # Clean up if save fails
        if os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to save file: {str(e)}"
        )


def delete_file(file_path: str) -> bool:
    """
    Delete file from disk
    
    Args:
        file_path: Path to file to delete
        
    Returns:
        True if deleted successfully, False otherwise
    """
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            return True
        return False
    except Exception:
        return False


def get_file_path_from_url(url_path: str, base_dir: str = "app") -> str:
    """
    Convert URL path to file system path
    
    Args:
        url_path: URL path (e.g., /static/covers/image.jpg)
        base_dir: Base directory (default: app)
        
    Returns:
        File system path
    """
    # Remove leading slash and convert to file path
    relative_path = url_path.lstrip("/")
    return os.path.join(base_dir, relative_path)

# from fastapi.responses import FileResponse

# @router.get("/download/{username}")
# def download_persona(username: str):
#     """
#     Serves the generated persona file as a downloadable .txt file
#     """
#     filepath = f"outputs/{username}_persona.txt"
#     if os.path.exists(filepath):
#         return FileResponse(path=filepath, filename=f"{username}_persona.txt", media_type='text/plain')
#     raise HTTPException(status_code=404, detail="Persona file not found")

import os
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

router = APIRouter()

@router.get("/download/{username}")
async def download_persona(username: str):
    """
    Endpoint to download the generated persona file by username
    
    eg.- If the URL: "https://www.reddit.com/user/spez/"
    
    > username: spez
    _______________________________________________________________

    Args:
        username (str): Reddit username used for persona generation

    Returns:
        FileResponse: Returns the .txt file as a download if found
    """
    file_path = f"outputs/{username}_persona.txt"

    if os.path.exists(file_path):
        return FileResponse(
            path=file_path,
            filename=f"{username}_persona.txt",
            media_type="text/plain"
        )
    
    raise HTTPException(status_code=404, detail="Persona file not found")

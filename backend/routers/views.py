from fastapi import APIRouter
from fastapi.responses import FileResponse

from pathlib import Path

router = APIRouter(tags=["views"])

@router.get("/")
async def read_root():
    BASE_DIR = Path(__file__).resolve().parent.parent
    return FileResponse(BASE_DIR / "templates/index.html")

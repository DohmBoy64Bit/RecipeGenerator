from fastapi import APIRouter
from fastapi.responses import FileResponse

from pathlib import Path

router = APIRouter(tags=["views"])

@router.get("/")
async def read_root():
    BASE_DIR = Path(__file__).resolve().parent.parent
    return FileResponse(BASE_DIR / "templates/index.html")

@router.get("/sitemap.xml")
async def get_sitemap():
    BASE_DIR = Path(__file__).resolve().parent.parent
    return FileResponse(BASE_DIR / "static/sitemap.xml", media_type="application/xml")

@router.get("/robots.txt")
async def get_robots():
    BASE_DIR = Path(__file__).resolve().parent.parent
    return FileResponse(BASE_DIR / "static/robots.txt", media_type="text/plain")

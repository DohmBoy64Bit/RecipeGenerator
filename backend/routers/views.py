from fastapi import APIRouter
from fastapi.responses import FileResponse

router = APIRouter(tags=["views"])

@router.get("/")
async def read_root():
    return FileResponse("e:/RecipeGenerator/backend/templates/index.html")

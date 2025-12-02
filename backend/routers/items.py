from fastapi import APIRouter, Depends
from typing import Dict
from backend.services.recipe_service import RecipeService
from backend.dependencies import get_recipe_service

router = APIRouter(prefix="/api/items", tags=["items"])

@router.get("", response_model=Dict)
async def get_items(service: RecipeService = Depends(get_recipe_service)):
    """Get all items data (shop seeds and traits)."""
    return service.get_items()

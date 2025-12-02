from fastapi import APIRouter, Depends
from typing import Dict
from backend.services.recipe_service import RecipeService
from backend.dependencies import get_recipe_service

router = APIRouter(prefix="/api/stats", tags=["stats"])

@router.get("", response_model=Dict)
async def get_stats(service: RecipeService = Depends(get_recipe_service)):
    """Get recipe statistics."""
    return service.get_stats()

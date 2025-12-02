from fastapi import APIRouter, Depends
from typing import List, Dict
from backend.services.recipe_service import RecipeService
from backend.dependencies import get_recipe_service

router = APIRouter(prefix="/api/recipes", tags=["recipes"])

@router.get("", response_model=List[Dict])
async def get_recipes(
    shop_only: bool = False,
    service: RecipeService = Depends(get_recipe_service)
):
    """Get all recipes, optionally filtered to shop seeds only."""
    if shop_only:
        recipes = service.get_shop_only_recipes()
    else:
        recipes = service.get_all_recipes()
    
    # Convert dict to list for API response
    return list(recipes.values())

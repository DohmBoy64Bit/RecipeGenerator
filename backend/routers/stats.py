from fastapi import APIRouter, Depends
from backend.models import ItemStats, DataStore
from backend.dependencies import get_data_store
from backend.routers.recipes import is_recipe_possible

router = APIRouter(prefix="/api/stats", tags=["stats"])

@router.get("", response_model=ItemStats)
async def get_stats(data_store: DataStore = Depends(get_data_store)):
    total = len(data_store.recipes)
    shop_only_count = 0
    for recipe in data_store.recipes.values():
        if is_recipe_possible(recipe, data_store.shop_seeds):
            shop_only_count += 1
            
    return ItemStats(total_recipes=total, shop_only_recipes=shop_only_count)

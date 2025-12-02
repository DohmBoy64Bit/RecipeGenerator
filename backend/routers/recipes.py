from fastapi import APIRouter, Depends, Query
from typing import List
from backend.models import Recipe, DataStore
from backend.dependencies import get_data_store

router = APIRouter(prefix="/api/recipes", tags=["recipes"])

def is_recipe_possible(recipe: Recipe, available_items: set) -> bool:
    for ingredient_name, possible_items in recipe.ingredients.items():
        if not any(item in available_items for item in possible_items):
            return False
    return True

@router.get("", response_model=List[Recipe])
async def get_recipes(
    shop_only: bool = False,
    data_store: DataStore = Depends(get_data_store)
):
    if not shop_only:
        return list(data_store.recipes.values())
    
    filtered_recipes = []
    for recipe in data_store.recipes.values():
        if is_recipe_possible(recipe, data_store.shop_seeds):
            # Filter ingredients to show only available items
            filtered_ingredients = {}
            for ing_name, items in recipe.ingredients.items():
                available = [i for i in items if i in data_store.shop_seeds]
                filtered_ingredients[ing_name] = available
            
            new_recipe = recipe.model_copy(update={"ingredients": filtered_ingredients})
            filtered_recipes.append(new_recipe)
            
    return filtered_recipes

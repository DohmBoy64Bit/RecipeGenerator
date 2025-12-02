from typing import List, Dict, Optional, Union, Set
from pydantic import BaseModel

class RecipeIngredient(BaseModel):
    name: str
    possible_items: List[str]

class Recipe(BaseModel):
    id: str
    name: str
    image_id: str
    ingredients: Dict[str, List[str]]  # Ingredient Name -> List of valid items
    results: List[str]
    base_time: int
    base_weight: float
    priority: int

class ItemStats(BaseModel):
    total_recipes: int
    shop_only_recipes: int

class DataStore(BaseModel):
    recipes: Dict[str, Recipe]
    traits: Dict[str, List[str]]  # Item -> Traits
    shop_seeds: Set[str]
    items_by_trait: Dict[str, List[str]] # Trait -> Items

"""
Recipe service for managing food recipes and resolving ingredient categories.
"""
import json
import logging
from pathlib import Path
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

class RecipeService:
    def __init__(self, data_dir: str = None):
        if data_dir:
            self.data_dir = Path(data_dir)
        else:
            self.data_dir = Path(__file__).resolve().parent.parent.parent / "data"
        self.recipes_data: Dict = {}
        self.cooking_data: Dict = {}
        self.traits_data: Dict = {}
        self.shop_seeds: List[str] = []
        self.category_to_items: Dict[str, List[str]] = {}
        self._load_data()
        self._build_category_mapping()
    
    def _load_data(self) -> None:
        """Load recipe, cooking, and traits data from JSON files."""
        try:
            # Load recipes data
            recipes_file = self.data_dir / "recipes.json"
            if recipes_file.exists():
                with open(recipes_file, 'r', encoding='utf-8') as f:
                    self.recipes_data = json.load(f)
                logger.info(f"Loaded {len(self.recipes_data)} recipes")
            
            # Load cooking data
            cooking_file = self.data_dir / "cooking.json"
            if cooking_file.exists():
                with open(cooking_file, 'r', encoding='utf-8') as f:
                    self.cooking_data = json.load(f)
                logger.info(f"Loaded {len(self.cooking_data)} cooking categories")
            
            # Load traits data
            traits_file = self.data_dir / "plant_traits.json"
            if traits_file.exists():
                with open(traits_file, 'r', encoding='utf-8') as f:
                    self.traits_data = json.load(f)
                logger.info(f"Loaded {len(self.traits_data)} plants with traits")
            
            # Load shop seeds data
            shop_seeds_file = self.data_dir / "shopseeds.json"
            if shop_seeds_file.exists():
                with open(shop_seeds_file, 'r', encoding='utf-8') as f:
                    shop_seeds_data = json.load(f)
                    self.shop_seeds = shop_seeds_data.get("shopseeds", [])
                logger.info(f"Loaded {len(self.shop_seeds)} shop seeds")
            
        except Exception as e:
            logger.error(f"Failed to load recipe data: {e}")
    
    def _build_category_mapping(self) -> None:
        """Build reverse mapping: category -> items from cooking.json."""
        try:
            self.category_to_items = dict(self.cooking_data)
            logger.info(f"Built category mapping for {len(self.category_to_items)} categories")
        except Exception as e:
            logger.error(f"Failed to build category mapping: {e}")
            self.category_to_items = {}
    
    def resolve_trait(self, trait: str) -> List[str]:
        """Return all items in traits.json that have a given trait."""
        return [item for item, ts in self.traits_data.items() if trait in ts]
    
    def resolve_herbalbase(self) -> List[str]:
        """Return flowers that are not toxic, plus Mint if available."""
        items = [item for item, ts in self.traits_data.items() 
                 if "Flower" in ts and "Toxic" not in ts]
        if "Mint" in self.traits_data:
            items.append("Mint")
        return list(set(items))
    
    def resolve_filling(self) -> List[str]:
        """Filling = all vegetables + meat items (composite category)."""
        vegetable_items = self.resolve_trait("Vegetable")
        meat_items = self.category_to_items.get("Meat", [])
        return list(set(vegetable_items + meat_items))
    
    def resolve_category(self, cat: str) -> List[str]:
        """
        Return all possible items for a category.
        Merges cooking.json fixed items and traits.json items for trait-based categories.
        """
        # Category resolvers
        CATEGORY_RESOLVERS = {
            "Bread": lambda: self.category_to_items.get("Bread", []),
            "Meat": lambda: self.category_to_items.get("Meat", []),
            "Leafy": lambda: self.category_to_items.get("Leafy", []),
            "Pastry": lambda: self.category_to_items.get("Pastry", []),
            "Tomato": lambda: self.category_to_items.get("Tomato", []),
            "Fruit": lambda: self.resolve_trait("Fruit"),
            "Vegetable": lambda: self.resolve_trait("Vegetable"),
            "Sweet": lambda: self.resolve_trait("Sweet"),
            "Sauce": lambda: self.resolve_trait("Fruit"),
            "Cone": lambda: self.category_to_items.get("Bread", []),
            "Cream": lambda: self.resolve_trait("Sweet"),
            "Base": lambda: self.category_to_items.get("Bread", []),
            "Stick": lambda: self.resolve_trait("Woody"),
            "Icing": lambda: self.resolve_trait("Sweet"),
            "Sprinkles": lambda: self.resolve_trait("Sweet"),
            "CandyCoating": lambda: self.resolve_trait("Sweet"),
            "Sweetener": lambda: self.resolve_trait("Sweet"),
            "HerbalBase": lambda: self.resolve_herbalbase(),
            "Filling": lambda: self.resolve_filling(),
            "Bamboo": lambda: self.category_to_items.get("Bamboo", []),
            "Wrap": lambda: self.category_to_items.get("Wrap", []),
            "Rice": lambda: self.category_to_items.get("Rice", []),
            "Woody": lambda: self.resolve_trait("Woody"),
            "Apple": lambda: self.category_to_items.get("Apple", []),
            "Batter": lambda: self.category_to_items.get("Batter", []),
            "Pasta": lambda: self.category_to_items.get("Pasta", []),
            "Vegetables": lambda: self.resolve_trait("Vegetable"),
            "Main": lambda: list(set(self.category_to_items.get("Meat", []) + self.resolve_trait("Vegetable"))),
            "Any": lambda: list(self.traits_data.keys())
        }
        
        resolver = CATEGORY_RESOLVERS.get(cat)
        items = resolver() if callable(resolver) else []
        
        # Merge with cooking.json fixed items if not already included
        fixed_items = self.category_to_items.get(cat, [])
        return list(set(items) | set(fixed_items))
    
    def get_all_recipes(self) -> Dict:
        """Get all available recipes with their ingredient categories resolved."""
        recipes_with_ingredients = {}
        
        for name, recipe in self.recipes_data.items():
            # Resolve each ingredient category to actual items
            ingredients = {}
            for category in recipe.get("ingredients", {}).keys():
                ingredients[category] = self.resolve_category(category)
            
            # Calculate total combinations
            combinations = 1
            for items in ingredients.values():
                if items:
                    combinations *= len(items)
                else:
                    combinations = 0

            # Format display name
            display_names = {
                "CandyApple": "Candy Apple",
                "HotDog": "Hot Dog",
                "IceCream": "Ice Cream",
                "SweetTea": "Sweet Tea",
                "Corndog": "Corn Dog"
            }
            display_name = display_names.get(name, name)

            recipes_with_ingredients[name] = {
                "id": recipe.get("id", ""),
                "name": display_name,
                "image_id": recipe.get("image_id", ""),
                "ingredients": ingredients,
                "results": [display_name],
                "base_time": recipe.get("base_time", 0),
                "base_weight": recipe.get("base_weight", 0.0),
                "combinations": combinations,
                "priority": recipe.get("priority", 0)
            }
        
        return recipes_with_ingredients
    
    def get_shop_only_recipes(self) -> Dict:
        """Get recipes that can be made with shop seeds only."""
        all_recipes = self.get_all_recipes()
        shop_recipes = {}
        
        for name, recipe in all_recipes.items():
            # Check if all ingredient categories have at least one shop seed
            can_make = True
            filtered_ingredients = {}
            
            for category, items in recipe["ingredients"].items():
                shop_items = [item for item in items if item in self.shop_seeds]
                if not shop_items:
                    can_make = False
                    break
                filtered_ingredients[category] = shop_items
            
            if can_make:
                recipe_copy = recipe.copy()
                recipe_copy["ingredients"] = filtered_ingredients
                
                # Recalculate combinations for shop-only version
                combinations = 1
                for items in filtered_ingredients.values():
                    combinations *= len(items)
                recipe_copy["combinations"] = combinations
                
                shop_recipes[name] = recipe_copy
        
        return shop_recipes
    
    def get_stats(self) -> Dict:
        """Get statistics about recipes."""
        all_recipes = self.get_all_recipes()
        shop_recipes = self.get_shop_only_recipes()
        
        # Get last updated time from metadata.json
        import json
        metadata_file = self.data_dir / "metadata.json"
        last_updated = None
        
        if metadata_file.exists():
            try:
                with open(metadata_file, 'r') as f:
                    data = json.load(f)
                    last_updated = data.get("last_updated")
            except Exception:
                pass
        
        # Fallback to recipes.json mtime if metadata doesn't exist (for backward compatibility)
        if not last_updated:
            recipes_file = self.data_dir / "recipes.json"
            if recipes_file.exists():
                from datetime import datetime
                mtime = recipes_file.stat().st_mtime
                dt = datetime.fromtimestamp(mtime)
                last_updated = dt.strftime("%m/%d/%Y %I:%M:%S %p")
        
        return {
            "total_recipes": len(all_recipes),
            "shop_only_recipes": len(shop_recipes),
            "last_updated": last_updated
        }
    
    def get_items(self) -> Dict:
        """Get all items data."""
        return {
            "shop_seeds": self.shop_seeds,
            "traits": self.traits_data
        }

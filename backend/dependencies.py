from backend.services.recipe_service import RecipeService

# Global instance
_recipe_service = RecipeService("e:/RecipeGenerator/data")

def load_global_data():
    """Load data on startup."""
    # RecipeService loads data in __init__, so this is just for compatibility
    print(f"RecipeService loaded {len(_recipe_service.recipes_data)} recipes")

def get_recipe_service() -> RecipeService:
    """Get the global RecipeService instance."""
    return _recipe_service

from backend.data_loader import DataLoader
import json

def test_loader():
    loader = DataLoader("e:/RecipeGenerator/data")
    data = loader.load_data()
    
    print(f"Loaded {len(data.recipes)} recipes.")
    print(f"Loaded {len(data.traits)} items with traits.")
    print(f"Loaded {len(data.shop_seeds)} shop seeds.")
    
    # Check specific recipe: Burger
    if "Burger" in data.recipes:
        burger = data.recipes["Burger"]
        print("\nRecipe: Burger")
        print(f"Ingredients: {json.dumps(burger.ingredients, indent=2)}")
    else:
        print("\nERROR: Burger recipe not found!")

    # Check specific recipe: Pie (uses MakeTable)
    if "Pie" in data.recipes:
        pie = data.recipes["Pie"]
        print("\nRecipe: Pie")
        print(f"Ingredients: {json.dumps(pie.ingredients, indent=2)}")
    else:
        print("\nERROR: Pie recipe not found!")

if __name__ == "__main__":
    test_loader()

import json
from typing import Dict, List, Set
from pathlib import Path
from backend.models import Recipe, DataStore

class DataLoader:
    def __init__(self, data_dir: str):
        self.data_dir = Path(data_dir)
        self.traits_file = self.data_dir / "plant_traits.json"
        self.shop_file = self.data_dir / "shopseeds.json"
        self.recipes_file = self.data_dir / "recipes.json"
        
        self.traits: Dict[str, List[str]] = {}
        self.items_by_trait: Dict[str, List[str]] = {}
        self.shop_seeds: Set[str] = set()
        self.recipes: Dict[str, Recipe] = {}
        
    def load_data(self) -> DataStore:
        self._load_traits()
        self._load_shop_seeds()
        self._load_recipes()
        
        return DataStore(
            recipes=self.recipes,
            traits=self.traits,
            shop_seeds=self.shop_seeds,
            items_by_trait=self.items_by_trait
        )

    def _load_traits(self):
        with open(self.traits_file, 'r') as f:
            self.traits = json.load(f)
            
        for item, trait_list in self.traits.items():
            for trait in trait_list:
                if trait not in self.items_by_trait:
                    self.items_by_trait[trait] = []
                self.items_by_trait[trait].append(item)

    def _load_shop_seeds(self):
        with open(self.shop_file, 'r') as f:
            data = json.load(f)
            self.shop_seeds = set(data.get("shopseeds", []))

    def _load_recipes(self):
        with open(self.recipes_file, 'r') as f:
            raw_recipes = json.load(f)
            
        for name, data in raw_recipes.items():
            self.recipes[name] = Recipe(**data)

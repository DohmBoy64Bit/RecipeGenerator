from backend.services.data_loader import DataLoader
from backend.models import DataStore

# Global instance
_data_loader = DataLoader("e:/RecipeGenerator/data")
_data_store: DataStore = None

def load_global_data():
    global _data_store
    _data_store = _data_loader.load_data()
    print(f"Loaded {len(_data_store.recipes)} recipes")

def get_data_store() -> DataStore:
    if _data_store is None:
        # Should be loaded on startup, but just in case
        load_global_data()
    return _data_store

from fastapi import APIRouter, Depends
from backend.models import DataStore
from backend.dependencies import get_data_store

router = APIRouter(prefix="/api/items", tags=["items"])

@router.get("")
async def get_items(data_store: DataStore = Depends(get_data_store)):
    return {
        "shop_seeds": list(data_store.shop_seeds),
        "traits": data_store.traits
    }

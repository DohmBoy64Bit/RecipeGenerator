from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from backend.dependencies import load_global_data
from backend.routers import recipes, stats, items, views

app = FastAPI(title="Recipe Generator API")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(recipes.router)
app.include_router(stats.router)
app.include_router(items.router)
app.include_router(views.router)

# Serve Static Files (if needed for assets, though index.html is served by views)
# We mount the templates dir as static too just in case, or for assets
app.mount("/static", StaticFiles(directory="e:/RecipeGenerator/backend/templates"), name="static")

@app.on_event("startup")
async def startup_event():
    load_global_data()

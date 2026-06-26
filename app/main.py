from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine
from app.routers import pokemon
from app.models import pokemon as pokemon_models

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Pokédex API",
    description="API REST para consultar información de los 151 Pokémon originales",
    version="1.0.0"
)

# CORS — permite que el frontend acceda a la API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.include_router(pokemon.router)

@app.get("/health")
def health_check():
    return {"status": "ok", "message": "Pokédex API funcionando correctamente"}
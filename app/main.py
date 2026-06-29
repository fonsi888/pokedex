from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from app.middleware import SecurityHeadersMiddleware
from starlette.templating import Jinja2Templates
from app.database import Base, engine
from app.routers import pokemon
from app.models import pokemon as pokemon_models
import os

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Pokédex API",
    description="API REST para consultar información de los 151 Pokémon originales",
    version="1.0.0"
)

app.add_middleware(SecurityHeadersMiddleware)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), "templates"))

app.include_router(pokemon.router)

@app.get("/health")
def health_check():
    return {"status": "ok", "message": "Pokédex API funcionando correctamente"}

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/pokemon/{pokemon_id}")
async def pokemon_detail(request: Request, pokemon_id: int):
    return templates.TemplateResponse(
        "pokemon_detail.html",
        {"request": request, "pokemon_id": pokemon_id}
    )
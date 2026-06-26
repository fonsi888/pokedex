from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from app.database import get_db
from app.services import pokemon as pokemon_service
from app.schemas.pokemon import PokemonListSchema, PokemonDetailSchema, TypeSchema
from app.models.pokemon import Pokemon, Evolution

router = APIRouter(prefix="/api", tags=["pokemon"])

@router.get("/pokemon", response_model=List[PokemonListSchema])
def get_all_pokemon(
    search: Optional[str] = Query(None, description="Buscar por nombre"),
    type_filter: Optional[str] = Query(None, description="Filtrar por tipo"),
    db: Session = Depends(get_db)
):
    """
    Devuelve la lista de Pokémon.
    - Opcional: buscar por nombre con ?search=pikachu
    - Opcional: filtrar por tipo con ?type_filter=fire
    """
    if search:
        return pokemon_service.search_pokemon(db, search)
    if type_filter:
        return pokemon_service.get_pokemon_by_type(db, type_filter)
    return pokemon_service.get_all_pokemon(db)

@router.get("/pokemon/{pokemon_id}", response_model=PokemonDetailSchema)
def get_pokemon(pokemon_id: int, db: Session = Depends(get_db)):
    """Devuelve el detalle completo de un Pokémon por su ID."""
    pokemon = pokemon_service.get_pokemon_by_id(db, pokemon_id)
    if not pokemon:
        raise HTTPException(status_code=404, detail="Pokémon no encontrado")
    return pokemon

@router.get("/types", response_model=List[TypeSchema])
def get_types(db: Session = Depends(get_db)):
    """Devuelve todos los tipos de Pokémon disponibles."""
    return pokemon_service.get_all_types(db)
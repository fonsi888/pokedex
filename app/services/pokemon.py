from sqlalchemy.orm import Session
from app.models.pokemon import Pokemon, Type
from typing import Optional, List

def get_all_pokemon(db: Session) -> List[Pokemon]:
    """Devuelve todos los Pokémon ordenados por ID."""
    return db.query(Pokemon).order_by(Pokemon.pokeapi_id).all()

def get_pokemon_by_id(db: Session, pokemon_id: int) -> Optional[Pokemon]:
    """Devuelve un Pokémon por su ID de PokéAPI."""
    return db.query(Pokemon).filter(Pokemon.pokeapi_id == pokemon_id).first()

def get_pokemon_by_name(db: Session, name: str) -> Optional[Pokemon]:
    """Devuelve un Pokémon por su nombre exacto."""
    return db.query(Pokemon).filter(Pokemon.name == name.lower()).first()

def search_pokemon(db: Session, query: str) -> List[Pokemon]:
    """Busca Pokémon cuyo nombre contenga el texto buscado."""
    return (
        db.query(Pokemon)
        .filter(Pokemon.name.ilike(f"%{query}%"))
        .order_by(Pokemon.pokeapi_id)
        .all()
    )

def get_pokemon_by_type(db: Session, type_name: str) -> List[Pokemon]:
    """Devuelve todos los Pokémon de un tipo concreto."""
    return (
        db.query(Pokemon)
        .join(Pokemon.types)
        .filter(Type.name == type_name.lower())
        .order_by(Pokemon.pokeapi_id)
        .all()
    )

def get_all_types(db: Session) -> List[Type]:
    """Devuelve todos los tipos disponibles."""
    return db.query(Type).order_by(Type.name).all()
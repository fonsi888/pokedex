from pydantic import BaseModel
from typing import Optional, List

class TypeSchema(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True

class StatsSchema(BaseModel):
    hp: int
    attack: int
    defense: int
    special_attack: int
    special_defense: int
    speed: int

    class Config:
        from_attributes = True

class EvolutionSchema(BaseModel):
    from_pokemon_id: int
    to_pokemon_id: int
    min_level: Optional[int]

    class Config:
        from_attributes = True

class PokemonListSchema(BaseModel):
    pokeapi_id: int
    name: str
    image_url: Optional[str]
    types: List[TypeSchema]

    class Config:
        from_attributes = True

class PokemonDetailSchema(BaseModel):
    pokeapi_id: int
    name: str
    height: int
    weight: int
    base_experience: Optional[int]
    image_url: Optional[str]
    description: Optional[str]
    types: List[TypeSchema]
    stats: Optional[StatsSchema]
    evolutions_from: List[EvolutionSchema] = []
    evolutions_to: List[EvolutionSchema] = []

    class Config:
        from_attributes = True
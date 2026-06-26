from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.database import Base

pokemon_types = Table(
    "pokemon_types",
    Base.metadata,
    Column("pokemon_id", Integer, ForeignKey("pokemon.id"), primary_key=True),
    Column("type_id", Integer, ForeignKey("types.id"), primary_key=True),
    Column("slot", Integer)
)

class Pokemon(Base):
    __tablename__ = "pokemon"
    
    id = Column(Integer, primary_key=True, index=True)
    pokeapi_id = Column(Integer, unique=True, index=True)
    name = Column(String(100), unique=True, index=True)
    height = Column(Integer)
    weight = Column(Integer)
    base_experience = Column(Integer)
    image_url = Column(String(500))
    description = Column(String(1000))
    
    stats = relationship("Stats", back_populates="pokemon", uselist=False)
    types = relationship("Type", secondary=pokemon_types, back_populates="pokemon")
    evolutions_from = relationship(
        "Evolution",
        foreign_keys="Evolution.from_pokemon_id",
        back_populates="from_pokemon"
    )
    evolutions_to = relationship(
        "Evolution",
        foreign_keys="Evolution.to_pokemon_id",
        back_populates="to_pokemon"
    )

class Type(Base):
    __tablename__ = "types"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, index=True)
    
    pokemon = relationship("Pokemon", secondary=pokemon_types, back_populates="types")

class Stats(Base):
    __tablename__ = "stats"
    
    id = Column(Integer, primary_key=True, index=True)
    pokemon_id = Column(Integer, ForeignKey("pokemon.id"), unique=True)
    hp = Column(Integer)
    attack = Column(Integer)
    defense = Column(Integer)
    special_attack = Column(Integer)
    special_defense = Column(Integer)
    speed = Column(Integer)
    
    pokemon = relationship("Pokemon", back_populates="stats")

class Evolution(Base):
    __tablename__ = "evolutions"
    
    id = Column(Integer, primary_key=True, index=True)
    from_pokemon_id = Column(Integer, ForeignKey("pokemon.id"))
    to_pokemon_id = Column(Integer, ForeignKey("pokemon.id"))
    min_level = Column(Integer, nullable=True)
    
    from_pokemon = relationship("Pokemon", foreign_keys=[from_pokemon_id], back_populates="evolutions_from")
    to_pokemon = relationship("Pokemon", foreign_keys=[to_pokemon_id], back_populates="evolutions_to")
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_db
from app.models.pokemon import Pokemon, Type, Stats, Evolution, pokemon_types

# Base de datos en memoria para tests — no toca la BD real
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session")
def db_engine():
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def db(db_engine):
    connection = db_engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture(scope="function")
def client(db):
    def override_get_db():
        yield db
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()

@pytest.fixture(scope="function")
def sample_pokemon(db):
    """Crea un Pokémon de prueba en la BD de test."""
    # Crear tipo
    fire_type = Type(name="fire")
    db.add(fire_type)
    db.flush()

    # Crear Pokémon
    pokemon = Pokemon(
        pokeapi_id=4,
        name="charmander",
        height=6,
        weight=85,
        base_experience=62,
        image_url="https://example.com/charmander.png",
        description="Un Pokémon de fuego."
    )
    db.add(pokemon)
    db.flush()

    # Añadir stats
    stats = Stats(
        pokemon_id=pokemon.id,
        hp=39,
        attack=52,
        defense=43,
        special_attack=60,
        special_defense=50,
        speed=65
    )
    db.add(stats)

    # Añadir tipo
    db.execute(
        pokemon_types.insert().values(
            pokemon_id=pokemon.id,
            type_id=fire_type.id,
            slot=1
        )
    )
    db.commit()
    return pokemon
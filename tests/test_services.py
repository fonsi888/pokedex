import pytest
from app.services.pokemon import (
    get_all_pokemon,
    get_pokemon_by_id,
    get_pokemon_by_name,
    search_pokemon,
    get_pokemon_by_type,
    get_all_types
)
from app.models.pokemon import Pokemon, Type

class TestGetAllPokemon:
    def test_returns_empty_list_when_no_pokemon(self, db):
        """Sin datos en BD devuelve lista vacía."""
        result = get_all_pokemon(db)
        assert result == []

    def test_returns_pokemon_when_exists(self, db, sample_pokemon):
        """Con datos devuelve la lista correcta."""
        result = get_all_pokemon(db)
        assert len(result) == 1
        assert result[0].name == "charmander"

    def test_returns_ordered_by_pokeapi_id(self, db):
        """Los Pokémon se devuelven ordenados por ID."""
        p2 = Pokemon(pokeapi_id=2, name="ivysaur", height=10, weight=130,
                     base_experience=142, image_url="", description="")
        p1 = Pokemon(pokeapi_id=1, name="bulbasaur", height=7, weight=69,
                     base_experience=64, image_url="", description="")
        db.add_all([p2, p1])
        db.commit()
        result = get_all_pokemon(db)
        assert result[0].pokeapi_id == 1
        assert result[1].pokeapi_id == 2


class TestGetPokemonById:
    def test_returns_pokemon_when_found(self, db, sample_pokemon):
        """Devuelve el Pokémon correcto por ID."""
        result = get_pokemon_by_id(db, 4)
        assert result is not None
        assert result.name == "charmander"
        assert result.pokeapi_id == 4

    def test_returns_none_when_not_found(self, db):
        """Devuelve None si el ID no existe."""
        result = get_pokemon_by_id(db, 9999)
        assert result is None

    def test_returns_correct_stats(self, db, sample_pokemon):
        """El Pokémon devuelto tiene sus stats."""
        result = get_pokemon_by_id(db, 4)
        assert result.stats is not None
        assert result.stats.hp == 39
        assert result.stats.attack == 52


class TestSearchPokemon:
    def test_search_by_partial_name(self, db, sample_pokemon):
        """Búsqueda parcial encuentra el Pokémon."""
        result = search_pokemon(db, "char")
        assert len(result) == 1
        assert result[0].name == "charmander"

    def test_search_case_insensitive(self, db, sample_pokemon):
        """La búsqueda no distingue mayúsculas."""
        result = search_pokemon(db, "CHAR")
        assert len(result) == 1

    def test_search_returns_empty_when_no_match(self, db, sample_pokemon):
        """Búsqueda sin coincidencias devuelve lista vacía."""
        result = search_pokemon(db, "pikachu")
        assert result == []


class TestGetPokemonByType:
    def test_filter_by_type(self, db, sample_pokemon):
        """Filtrar por tipo devuelve los correctos."""
        result = get_pokemon_by_type(db, "fire")
        assert len(result) == 1
        assert result[0].name == "charmander"

    def test_filter_returns_empty_for_unknown_type(self, db, sample_pokemon):
        """Tipo inexistente devuelve lista vacía."""
        result = get_pokemon_by_type(db, "dragon")
        assert result == []


class TestGetAllTypes:
    def test_returns_all_types(self, db, sample_pokemon):
        """Devuelve todos los tipos disponibles."""
        result = get_all_types(db)
        assert len(result) >= 1
        type_names = [t.name for t in result]
        assert "fire" in type_names
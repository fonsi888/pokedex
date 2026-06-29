import pytest

class TestHealthEndpoint:
    def test_health_check_returns_ok(self, client):
        """El endpoint de salud responde correctamente."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"


class TestPokemonListEndpoint:
    def test_get_all_pokemon_empty(self, client):
        """Sin datos devuelve lista vacía."""
        response = client.get("/api/pokemon")
        assert response.status_code == 200
        assert response.json() == []

    def test_get_all_pokemon_with_data(self, client, sample_pokemon):
        """Con datos devuelve la lista."""
        response = client.get("/api/pokemon")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["name"] == "charmander"

    def test_search_pokemon(self, client, sample_pokemon):
        """La búsqueda por nombre funciona."""
        response = client.get("/api/pokemon?search=char")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["name"] == "charmander"

    def test_filter_by_type(self, client, sample_pokemon):
        """El filtro por tipo funciona."""
        response = client.get("/api/pokemon?type_filter=fire")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1

    def test_search_no_results(self, client, sample_pokemon):
        """Búsqueda sin resultados devuelve lista vacía."""
        response = client.get("/api/pokemon?search=zzzzz")
        assert response.status_code == 200
        assert response.json() == []


class TestPokemonDetailEndpoint:
    def test_get_existing_pokemon(self, client, sample_pokemon):
        """Devuelve el detalle de un Pokémon existente."""
        response = client.get("/api/pokemon/4")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "charmander"
        assert data["pokeapi_id"] == 4
        assert data["stats"]["hp"] == 39

    def test_get_nonexistent_pokemon_returns_404(self, client):
        """Pokémon inexistente devuelve 404."""
        response = client.get("/api/pokemon/9999")
        assert response.status_code == 404
        assert "no encontrado" in response.json()["detail"]

    def test_pokemon_has_required_fields(self, client, sample_pokemon):
        """La respuesta tiene todos los campos necesarios."""
        response = client.get("/api/pokemon/4")
        data = response.json()
        required_fields = ["pokeapi_id", "name", "height", "weight",
                          "types", "stats", "description"]
        for field in required_fields:
            assert field in data, f"Falta el campo: {field}"


class TestTypesEndpoint:
    def test_get_types_returns_list(self, client, sample_pokemon):
        """El endpoint de tipos devuelve una lista."""
        response = client.get("/api/types")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1

    def test_types_have_required_fields(self, client, sample_pokemon):
        """Cada tipo tiene id y name."""
        response = client.get("/api/types")
        data = response.json()
        for type_item in data:
            assert "id" in type_item
            assert "name" in type_item
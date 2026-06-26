import sys
import os
import time
import requests

# Añadir el directorio raíz al path para importar los módulos de la app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal, engine
from app.models.pokemon import Base, Pokemon, Type, Stats, Evolution, pokemon_types

# Crear todas las tablas si no existen
Base.metadata.create_all(bind=engine)

POKEAPI_BASE = "https://pokeapi.co/api/v2"
TOTAL_POKEMON = 151


def get_json(url: str) -> dict:
    """Hace una petición GET y devuelve el JSON. Reintenta si falla."""
    for attempt in range(3):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"  ⚠️  Error en {url} (intento {attempt + 1}/3): {e}")
            time.sleep(2)
    raise Exception(f"No se pudo obtener datos de {url}")


def get_or_create_type(db, type_name: str) -> Type:
    """Busca un tipo en la BD o lo crea si no existe."""
    pokemon_type = db.query(Type).filter(Type.name == type_name).first()
    if not pokemon_type:
        pokemon_type = Type(name=type_name)
        db.add(pokemon_type)
        db.flush()
    return pokemon_type


def get_description(species_url: str) -> str:
    """Obtiene la descripción en español o inglés del Pokémon."""
    try:
        data = get_json(species_url)
        # Buscar descripción en español primero
        for entry in data.get("flavor_text_entries", []):
            if entry["language"]["name"] == "es":
                return entry["flavor_text"].replace("\n", " ").replace("\f", " ")
        # Si no hay español, usar inglés
        for entry in data.get("flavor_text_entries", []):
            if entry["language"]["name"] == "en":
                return entry["flavor_text"].replace("\n", " ").replace("\f", " ")
    except Exception:
        pass
    return "Descripción no disponible."


def get_evolution_chain(chain_url: str) -> list:
    """Extrae la cadena de evoluciones como lista de tuplas (desde, hasta, nivel)."""
    evolutions = []
    try:
        data = get_json(chain_url)
        chain = data.get("chain", {})

        def traverse(node, previous_name=None):
            current_name = node["species"]["name"]
            if previous_name:
                min_level = None
                details = node.get("evolution_details", [])
                if details and details[0].get("min_level"):
                    min_level = details[0]["min_level"]
                evolutions.append((previous_name, current_name, min_level))
            for next_evolution in node.get("evolves_to", []):
                traverse(next_evolution, current_name)

        traverse(chain)
    except Exception as e:
        print(f"  ⚠️  Error procesando cadena de evolución: {e}")
    return evolutions


def load_pokemon():
    """Función principal: descarga e inserta los 151 Pokémon."""
    db = SessionLocal()

    try:
        # Verificar si ya hay datos
        existing = db.query(Pokemon).count()
        if existing > 0:
            print(f"⚠️  Ya hay {existing} Pokémon en la base de datos.")
            print("   Si quieres recargar, borra los datos primero.")
            return

        print(f"🚀 Iniciando carga de {TOTAL_POKEMON} Pokémon...\n")

        # Guardar cadenas de evolución para procesarlas al final
        evolution_chains = []

        for pokemon_id in range(1, TOTAL_POKEMON + 1):
            try:
                print(f"📥 [{pokemon_id:03d}/{TOTAL_POKEMON}] Descargando datos...", end=" ")

                # Datos principales del Pokémon
                data = get_json(f"{POKEAPI_BASE}/pokemon/{pokemon_id}")
                species_data = get_json(data["species"]["url"])

                # Descripción
                description = get_description(data["species"]["url"])

                # Imagen oficial
                image_url = (
                    data.get("sprites", {})
                    .get("other", {})
                    .get("official-artwork", {})
                    .get("front_default", "")
                )

                # Crear el Pokémon
                pokemon = Pokemon(
                    pokeapi_id=pokemon_id,
                    name=data["name"],
                    height=data["height"],
                    weight=data["weight"],
                    base_experience=data.get("base_experience", 0),
                    image_url=image_url,
                    description=description
                )
                db.add(pokemon)
                db.flush()  # Para obtener el ID generado

                # Stats
                stats_map = {s["stat"]["name"]: s["base_stat"] for s in data["stats"]}
                stats = Stats(
                    pokemon_id=pokemon.id,
                    hp=stats_map.get("hp", 0),
                    attack=stats_map.get("attack", 0),
                    defense=stats_map.get("defense", 0),
                    special_attack=stats_map.get("special-attack", 0),
                    special_defense=stats_map.get("special-defense", 0),
                    speed=stats_map.get("speed", 0)
                )
                db.add(stats)

                # Tipos
                for type_info in data["types"]:
                    type_name = type_info["type"]["name"]
                    slot = type_info["slot"]
                    pokemon_type = get_or_create_type(db, type_name)
                    db.execute(
                        pokemon_types.insert().values(
                            pokemon_id=pokemon.id,
                            type_id=pokemon_type.id,
                            slot=slot
                        )
                    )

                # Guardar cadena de evolución para después
                evolution_url = species_data.get("evolution_chain", {}).get("url")
                if evolution_url:
                    evolution_chains.append(evolution_url)

                db.commit()
                print(f"✅ {data['name'].capitalize()}")

                # Pausa pequeña para no saturar la PokéAPI
                time.sleep(0.3)

            except Exception as e:
                db.rollback()
                print(f"❌ Error con Pokémon {pokemon_id}: {e}")
                continue

        # Procesar evoluciones al final (cuando todos los Pokémon ya están en BD)
        print("\n🔗 Procesando cadenas de evolución...")
        processed_chains = set()

        for chain_url in evolution_chains:
            if chain_url in processed_chains:
                continue
            processed_chains.add(chain_url)

            evolutions = get_evolution_chain(chain_url)
            for from_name, to_name, min_level in evolutions:
                try:
                    from_pokemon = db.query(Pokemon).filter(Pokemon.name == from_name).first()
                    to_pokemon = db.query(Pokemon).filter(Pokemon.name == to_name).first()

                    if from_pokemon and to_pokemon:
                        # Verificar que no existe ya
                        existing_evo = db.query(Evolution).filter(
                            Evolution.from_pokemon_id == from_pokemon.id,
                            Evolution.to_pokemon_id == to_pokemon.id
                        ).first()

                        if not existing_evo:
                            evolution = Evolution(
                                from_pokemon_id=from_pokemon.id,
                                to_pokemon_id=to_pokemon.id,
                                min_level=min_level
                            )
                            db.add(evolution)
                except Exception as e:
                    print(f"  ⚠️  Error en evolución {from_name} → {to_name}: {e}")
                    continue

        db.commit()
        print("✅ Evoluciones procesadas correctamente.")

        # Resumen final
        total = db.query(Pokemon).count()
        print(f"\n🎉 ¡Carga completada! {total} Pokémon en la base de datos.")

    except Exception as e:
        db.rollback()
        print(f"\n❌ Error crítico: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    load_pokemon()
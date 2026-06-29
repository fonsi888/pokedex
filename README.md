# Pokédex Web

Aplicación web para consultar información sobre los 151 Pokémon de la primera generación.

## URL en Producción

https://pokedex-production-98d9.up.railway.app/

## Tecnologías

- **Backend**: Python 3.14 + FastAPI
- **Base de datos**: PostgreSQL + SQLAlchemy ORM
- **Frontend**: HTML5 + CSS3 + JavaScript vanilla
- **Despliegue**: Railway
- **Datos**: PokéAPI (carga inicial ETL)

## Funcionalidades

- Listado de los 151 Pokémon originales con imagen y tipo
- Búsqueda por nombre en tiempo real
- Filtro por tipo de Pokémon
- Ficha detallada con estadísticas, altura, peso y descripción
- Cadena de evoluciones
- API REST documentada en /docs

## Arquitectura

Frontend (HTML/CSS/JS)

↓

FastAPI (Backend Python)

↓

PostgreSQL (Base de datos)


## Instalación local

```bash
# 1. Clonar el repositorio
git clone https://github.com/fonsi888/pokedex.git
cd pokedex

# 2. Crear entorno virtual
python -m venv venv
venv\Scripts\activate  # Windows

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar variables de entorno
cp .env.example .env
# Editar .env con tus credenciales

# 5. Poblar la base de datos
python scripts/etl.py

# 6. Arrancar el servidor
uvicorn app.main:app --reload
```

## Testing

```bash
pytest tests/ -v
```

23 tests — 100% passing.

## Estructura del Proyecto

pokedex/

├── app/

│   ├── main.py          # Punto de entrada FastAPI

│   ├── config.py        # Configuración

│   ├── database.py      # Conexión PostgreSQL

│   ├── models/          # Modelos SQLAlchemy

│   ├── schemas/         # Validación Pydantic

│   ├── routers/         # Endpoints API

│   ├── services/        # Lógica de negocio

│   ├── static/          # CSS y JS

│   └── templates/       # HTML Jinja2

├── scripts/

│   └── etl.py           # Carga de datos desde PokéAPI

├── tests/               # Tests unitarios e integración

└── requirements.txt


## API Endpoints

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | /api/pokemon | Lista todos los Pokémon |
| GET | /api/pokemon/{id} | Detalle de un Pokémon |
| GET | /api/pokemon?search= | Búsqueda por nombre |
| GET | /api/pokemon?type_filter= | Filtro por tipo |
| GET | /api/types | Lista todos los tipos |
| GET | /health | Estado de la API |
| GET | /docs | Documentación Swagger |

## Seguridad

- Cabeceras HTTP de seguridad (X-Frame-Options, CSP, HSTS)
- Variables de entorno para credenciales
- Validación de datos con Pydantic
- ORM para prevención de SQL injection
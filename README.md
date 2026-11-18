# Buscaminas

Buscaminas (Minesweeper) jugable en el navegador, construido con Python, Flask y JavaScript.

## Arquitectura

El código está organizado por capas, de más independiente a más acoplada al framework web:

```
app/
  domain/                Lógica pura del juego (sin Flask, sin HTTP)
    types.py               Tipos: Cell, Board, Difficulty, GameStatus...
    board.py               Creación del tablero y colocación de minas
    gameplay.py            Revelar celdas (flood fill), marcar banderas, condición de victoria
    engine.py              MinesweeperEngine: orquesta una partida completa (estado + reglas)
    random_source.py       PRNG determinístico (seed) para partidas reproducibles
    difficulty.py          Niveles de dificultad predefinidos

  game_store.py          Guarda una instancia de MinesweeperEngine en memoria por partida
  game_url_params.py      Lee ?difficulty= y ?seed= de la query string
  serializers.py          Convierte el estado del dominio a JSON para el cliente
  routes.py               Endpoints Flask: /, /api/reveal, /api/flag, /api/reset

  templates/index.html    Página HTML (el tablero se pinta en el cliente)
  static/style.css        Estilos
  static/game.js          Pinta el tablero y llama a la API vía fetch
```

La regla de "primer click siempre seguro" se implementa colocando las minas recién
después del primer click, excluyendo esa celda y sus vecinas — igual que en la versión
original en TypeScript.

El estado de cada partida vive en el servidor (una instancia de `MinesweeperEngine` por
sesión de navegador, guardada en memoria). El cliente es una página con JavaScript sin
frameworks que llama a `/api/reveal`, `/api/flag` y `/api/reset` y vuelve a pintar el
tablero con la respuesta.

## Cómo correr el proyecto

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
playwright install chromium   # solo si vas a correr los tests e2e

python main.py        # http://localhost:5173
```

Se puede compartir o reproducir una partida exacta agregando `?seed=123` a la URL
(y opcionalmente `?difficulty=beginner|intermediate|expert`).

## Tests

Hay tres niveles de pruebas:

```bash
pytest                    # Unitarios (dominio) + integración (rutas Flask)
pytest e2e                # End-to-end en navegador real — Playwright
```

Para mostrar los tests e2e en clase, con el navegador visible y en cámara lenta:

```bash
pytest e2e --headed --slowmo 500 -s
```

- **Unitarios** (`tests/unit`): funciones puras del dominio (colocación de minas,
  flood fill, condición de victoria, motor del juego), sin Flask.
- **Integración** (`tests/integration`): las rutas Flask ejercitadas con el test
  client, verificando sesión, serialización y transiciones de estado completas.
- **End-to-end** (`e2e/`): flujo completo en un navegador real con Playwright,
  incluyendo escenarios determinísticos de "ganar" y "perder" gracias al seed del PRNG.

## Performance testing

Test de carga con [Locust](https://locust.io) (`perf/locustfile.py`), simulando
usuarios que abren una partida y hacen `reveal`/`flag`/`reset` contra la API.

```bash
pip install -r perf/requirements.txt

# gunicorn con 1 solo worker: el estado de las partidas vive en un dict en
# memoria por proceso, así que con más de 1 worker algunos requests caerían
# en un worker que no conoce el game_id de la sesión
gunicorn -w 1 -b 127.0.0.1:5173 "main:app"
```

En otra terminal, modo interactivo con UI web (`http://localhost:8089`):

```bash
locust -f perf/locustfile.py --host http://127.0.0.1:5173
```

O headless con reporte HTML (ej. 100 usuarios, 2 minutos):

```bash
locust -f perf/locustfile.py --host http://127.0.0.1:5173 \
  --headless -u 100 -r 10 -t 2m --html perf/report.html
```

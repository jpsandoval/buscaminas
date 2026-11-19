"""GET / — la página principal del juego.

Estos tests verifican que la ruta de inicio arma el tablero con la
dificultad correcta y respeta los parámetros de la URL (`difficulty` y
`seed`) que el resto de la app usa para compartir y reproducir partidas.
"""

from app.domain import Difficulty

DEFAULT_DIFFICULTY = Difficulty.default()


def test_renders_the_default_difficulty_when_no_query_params_are_given(client):
    # Arrange: no pasamos ningún parámetro -> debe usarse la dificultad default

    # Act
    response = client.get("/")

    # Assert
    assert response.status_code == 200
    body = response.get_data(as_text=True)
    assert "Buscaminas" in body
    assert f'data-testid="difficulty-{DEFAULT_DIFFICULTY.id}"' in body


def test_honors_the_difficulty_and_seed_query_params(client):
    # Arrange: pedimos explícitamente dificultad "expert" con una seed fija

    # Act
    response = client.get("/?difficulty=expert&seed=123")

    # Assert
    body = response.get_data(as_text=True)
    assert 'data-testid="difficulty-expert"' in body

"""POST /api/reveal — revelar una celda del tablero.

El caso más importante acá es la regla de "primer click siempre seguro":
nunca debería poder perderse en el primer click de una partida, sin
importar dónde se haga.
"""

SEED = 123
FIRST_CLICK = {"row": 0, "col": 0}


def test_the_first_click_of_a_game_is_always_safe(client):
    # Arrange: arrancamos una partida reproducible con una seed fija
    client.get(f"/?seed={SEED}")

    # Act: el primer click de la partida
    response = client.post("/api/reveal", json=FIRST_CLICK)

    # Assert: la partida pasa a "playing" y la celda clickeada queda revelada
    data = response.get_json()
    assert data["status"] == "playing"
    assert data["board"][0][0]["hasMine"] is False
    assert data["board"][0][0]["state"] == "revealed"

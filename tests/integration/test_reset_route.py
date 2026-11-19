"""POST /api/reset — reiniciar la partida actual.

Reiniciar puede, opcionalmente, cambiar de dificultad. Si no se pide una
dificultad nueva, debe conservar la que estaba jugándose.
"""

SEED = 123
FIRST_CLICK = {"row": 0, "col": 0}


def test_reset_can_switch_to_a_different_difficulty(client):
    # Arrange
    client.get(f"/?seed={SEED}")

    # Act: reiniciamos pidiendo explícitamente la dificultad "expert"
    response = client.post("/api/reset", json={"difficultyId": "expert"})

    # Assert: el tablero nuevo tiene el tamaño de "expert" (16 filas x 30 columnas)
    data = response.get_json()
    assert data["difficulty"]["id"] == "expert"
    assert len(data["board"]) == 16
    assert len(data["board"][0]) == 30
    assert data["status"] == "ready"


def test_reset_without_a_difficulty_keeps_the_current_one(client):
    # Arrange: empezamos una partida en "intermediate" y la jugamos un poco
    client.get(f"/?seed={SEED}&difficulty=intermediate")
    client.post("/api/reveal", json=FIRST_CLICK)

    # Act: reiniciamos sin indicar ninguna dificultad
    response = client.post("/api/reset", json={})

    # Assert: la dificultad se mantiene en "intermediate"
    data = response.get_json()
    assert data["difficulty"]["id"] == "intermediate"
    assert data["status"] == "ready"

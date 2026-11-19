"""POST /api/flag — marcar y desmarcar una celda con una bandera.

Marcar una celda no solo cambia su estado: también debe actualizar el
contador de minas restantes (minas totales - banderas puestas), que es
lo que el jugador ve en pantalla.
"""

from app.domain import Difficulty

SEED = 123
A_HIDDEN_CELL = {"row": 8, "col": 8}
DEFAULT_DIFFICULTY = Difficulty.default()


def test_flagging_a_hidden_cell_marks_it_and_decreases_mines_remaining(client):
    # Arrange
    client.get(f"/?seed={SEED}")

    # Act: marcamos una celda oculta con una bandera
    response = client.post("/api/flag", json=A_HIDDEN_CELL)

    # Assert
    data = response.get_json()
    assert data["board"][8][8]["state"] == "flagged"
    assert data["minesRemaining"] == DEFAULT_DIFFICULTY.mines - 1


def test_flagging_an_already_flagged_cell_removes_the_flag(client):
    # Arrange: la celda ya tiene una bandera puesta
    client.get(f"/?seed={SEED}")
    client.post("/api/flag", json=A_HIDDEN_CELL)

    # Act: marcamos la misma celda una segunda vez
    response = client.post("/api/flag", json=A_HIDDEN_CELL)

    # Assert: la bandera se quita y la celda vuelve a estar oculta
    data = response.get_json()
    assert data["board"][8][8]["state"] == "hidden"

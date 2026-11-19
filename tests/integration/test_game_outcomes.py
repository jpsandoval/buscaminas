"""Cómo termina una partida: perdiendo al revelar una mina, o ganando al
revelar todas las celdas seguras.

A diferencia de los tests anteriores, que prueban un solo endpoint de
forma aislada, estos tests encadenan varias llamadas a /api/reveal para
reproducir una partida completa de principio a fin.
"""

SEED = 123
FIRST_CLICK = {"row": 0, "col": 0}


def _mine_positions(board):
    return [
        (row, col)
        for row, cells in enumerate(board)
        for col, cell in enumerate(cells)
        if cell["hasMine"]
    ]


def test_revealing_a_mine_ends_the_game_and_reveals_every_mine(client):
    # Arrange: el primer click siempre es seguro, así que nos sirve para
    # conocer dónde quedaron las minas en esta partida
    client.get(f"/?seed={SEED}")
    first_click = client.post("/api/reveal", json=FIRST_CLICK).get_json()
    mine_positions = _mine_positions(first_click["board"])

    # Act: revelamos a propósito la primera mina que encontramos
    target_row, target_col = mine_positions[0]
    response = client.post("/api/reveal", json={"row": target_row, "col": target_col})

    # Assert: la partida termina en "lost" y TODAS las minas quedan reveladas,
    # no solo la que pisamos
    data = response.get_json()
    assert data["status"] == "lost"
    for row, col in mine_positions:
        assert data["board"][row][col]["state"] == "revealed"


def test_revealing_every_safe_cell_wins_the_game(client):
    # Arrange
    client.get(f"/?seed={SEED}")
    state = client.post("/api/reveal", json=FIRST_CLICK).get_json()
    mine_positions = set(_mine_positions(state["board"]))

    all_positions = [
        (row, col)
        for row in range(len(state["board"]))
        for col in range(len(state["board"][0]))
    ]
    safe_positions = [pos for pos in all_positions if pos not in mine_positions]

    # Act: revelamos, una por una, todas las celdas que no son minas
    for row, col in safe_positions:
        if state["board"][row][col]["state"] == "hidden":
            state = client.post("/api/reveal", json={"row": row, "col": col}).get_json()

    # Assert
    assert state["status"] == "won"

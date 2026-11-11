from app import create_app
from app.domain import Difficulty

DEFAULT_DIFFICULTY = Difficulty.default()


def make_client():
    app = create_app()
    app.config.update(TESTING=True)
    return app.test_client()


def test_index_renders_the_default_difficulty_board():
    client = make_client()

    response = client.get("/")

    assert response.status_code == 200
    body = response.get_data(as_text=True)
    assert "Buscaminas" in body
    assert f'data-testid="difficulty-{DEFAULT_DIFFICULTY.id}"' in body


def test_index_honors_difficulty_and_seed_query_params():
    client = make_client()

    response = client.get("/?difficulty=expert&seed=123")

    body = response.get_data(as_text=True)
    assert 'data-testid="difficulty-expert"' in body


def test_reveal_endpoint_starts_the_game_and_is_safe_on_first_click():
    client = make_client()
    client.get("/?seed=123")

    response = client.post("/api/reveal", json={"row": 0, "col": 0})

    data = response.get_json()
    assert data["status"] == "playing"
    assert data["board"][0][0]["hasMine"] is False
    assert data["board"][0][0]["state"] == "revealed"


def test_flag_endpoint_toggles_a_flag_and_updates_mines_remaining():
    client = make_client()
    client.get("/?seed=123")

    flagged = client.post("/api/flag", json={"row": 8, "col": 8}).get_json()
    assert flagged["board"][8][8]["state"] == "flagged"
    assert flagged["minesRemaining"] == DEFAULT_DIFFICULTY.mines - 1

    unflagged = client.post("/api/flag", json={"row": 8, "col": 8}).get_json()
    assert unflagged["board"][8][8]["state"] == "hidden"


def test_reset_endpoint_switches_difficulty_and_rebuilds_the_board():
    client = make_client()
    client.get("/?seed=123")

    data = client.post("/api/reset", json={"difficultyId": "expert"}).get_json()

    assert data["difficulty"]["id"] == "expert"
    assert len(data["board"]) == 16
    assert len(data["board"][0]) == 30
    assert data["status"] == "ready"


def test_reset_endpoint_without_difficulty_keeps_the_current_one():
    client = make_client()
    client.get("/?seed=123&difficulty=intermediate")
    client.post("/api/reveal", json={"row": 0, "col": 0})

    data = client.post("/api/reset", json={}).get_json()

    assert data["difficulty"]["id"] == "intermediate"
    assert data["status"] == "ready"


def test_losing_reveals_every_mine():
    client = make_client()
    client.get("/?seed=123")

    first_click = client.post("/api/reveal", json={"row": 0, "col": 0}).get_json()
    mine_positions = [
        (row, col)
        for row, cells in enumerate(first_click["board"])
        for col, cell in enumerate(cells)
        if cell["hasMine"]
    ]

    target_row, target_col = mine_positions[0]
    lost = client.post("/api/reveal", json={"row": target_row, "col": target_col}).get_json()

    assert lost["status"] == "lost"
    for row, col in mine_positions:
        assert lost["board"][row][col]["state"] == "revealed"


def test_winning_reveals_every_safe_cell():
    client = make_client()
    client.get("/?seed=123")

    state = client.post("/api/reveal", json={"row": 0, "col": 0}).get_json()
    safe_positions = [
        (row, col)
        for row, cells in enumerate(state["board"])
        for col, cell in enumerate(cells)
        if not cell["hasMine"]
    ]

    for row, col in safe_positions:
        cell = state["board"][row][col]
        if cell["state"] == "hidden":
            state = client.post("/api/reveal", json={"row": row, "col": col}).get_json()

    assert state["status"] == "won"

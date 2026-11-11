from __future__ import annotations

from flask import Blueprint, jsonify, render_template, request, session

from .domain import Difficulty, Position, SeededRandomSource
from .game_store import create_game, discard_game, get_game
from .game_url_params import read_game_url_params
from .serializers import serialize_state

bp = Blueprint("game", __name__)


@bp.get("/")
def index():
    params = read_game_url_params(request.args)
    random = SeededRandomSource(params.seed) if params.seed is not None else None

    discard_game(session.get("game_id"))
    game_id, engine = create_game(params.difficulty, random)
    session["game_id"] = game_id

    return render_template(
        "index.html",
        difficulties=Difficulty.all(),
        initial_state=serialize_state(engine.get_state()),
    )


@bp.post("/api/reveal")
def reveal():
    engine = get_game(session.get("game_id"))
    if engine is None:
        return jsonify({"error": "no_active_game"}), 404

    payload = request.get_json(silent=True) or {}
    position = Position(row=int(payload["row"]), col=int(payload["col"]))
    state = engine.reveal(position)
    return jsonify(serialize_state(state))


@bp.post("/api/flag")
def flag():
    engine = get_game(session.get("game_id"))
    if engine is None:
        return jsonify({"error": "no_active_game"}), 404

    payload = request.get_json(silent=True) or {}
    position = Position(row=int(payload["row"]), col=int(payload["col"]))
    state = engine.toggle_flag(position)
    return jsonify(serialize_state(state))


@bp.post("/api/reset")
def reset():
    engine = get_game(session.get("game_id"))
    current_difficulty = engine.get_state().difficulty if engine else Difficulty.default()

    payload = request.get_json(silent=True) or {}
    difficulty_id = payload.get("difficultyId")
    difficulty = (difficulty_id and Difficulty.find_by_id(difficulty_id)) or current_difficulty

    discard_game(session.get("game_id"))
    game_id, new_engine = create_game(difficulty)
    session["game_id"] = game_id

    return jsonify(serialize_state(new_engine.get_state()))

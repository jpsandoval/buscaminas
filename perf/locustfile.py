"""Load test for Buscaminas.

Simula usuarios que abren el tablero y juegan: revelan celdas, marcan
banderas y de vez en cuando reinician la partida.

Uso:
    pip install locust
    python main.py                       # o gunicorn, ver README de perf/
    locust -f perf/locustfile.py --host http://localhost:5173
"""

import random

from locust import HttpUser, between, task

DIFFICULTIES = {
    "beginner": (9, 9),
    "intermediate": (16, 16),
    "expert": (16, 30),
}


class MinesweeperPlayer(HttpUser):
    wait_time = between(0.5, 2.0)

    def on_start(self):
        self.difficulty = "beginner"
        self._new_game()

    def _new_game(self):
        rows, cols = DIFFICULTIES[self.difficulty]
        self.rows, self.cols = rows, cols
        self.client.get(f"/?difficulty={self.difficulty}", name="/ (index)")

    def _random_position(self):
        return {"row": random.randrange(self.rows), "col": random.randrange(self.cols)}

    @task(10)
    def reveal(self):
        self.client.post("/api/reveal", json=self._random_position())

    @task(3)
    def flag(self):
        self.client.post("/api/flag", json=self._random_position())

    @task(1)
    def reset(self):
        self.difficulty = random.choice(list(DIFFICULTIES))
        self.rows, self.cols = DIFFICULTIES[self.difficulty]
        self.client.post("/api/reset", json={"difficultyId": self.difficulty})

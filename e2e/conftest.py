import threading

import pytest
from werkzeug.serving import make_server

from app import create_app


@pytest.fixture(scope="session")
def live_server_url():
    app = create_app()
    server = make_server("127.0.0.1", 0, app)
    port = server.server_port
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()

    yield f"http://127.0.0.1:{port}"

    server.shutdown()
    thread.join()


@pytest.fixture(scope="session")
def base_url(live_server_url):
    return live_server_url

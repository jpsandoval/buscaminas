"""Fixtures compartidas por los tests de integración.

Estos tests ejercitan la aplicación Flask completa (rutas + sesión) a
través del test client de Flask, sin necesidad de levantar un servidor
real ni un navegador (eso es lo que hacen los tests end-to-end en e2e/).
"""

import pytest

from app import create_app


@pytest.fixture
def client():
    """Un cliente de pruebas con una app Flask nueva para cada test.

    Como cada test recibe su propia app, no hay estado compartido entre
    tests: uno no puede "ensuciar" la partida de otro.
    """
    app = create_app()
    app.config.update(TESTING=True)
    return app.test_client()

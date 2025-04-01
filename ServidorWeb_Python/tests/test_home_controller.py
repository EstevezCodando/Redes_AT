import pytest
from app import create_app

@pytest.fixture
def client():
    """
    Fixture que cria e configura uma instância de teste do nosso servidor Flask.
    """
    app = create_app()
    app.testing = True
    with app.test_client() as client:
        yield client

def test_get_index(client):
    """
    Testa uma requisição GET à rota principal.
    Verifica se o status code é 200 e se o HTML contém as informações esperadas.
    """
    response = client.get("/")
    assert response.status_code == 200
    assert b"Estado atual:" in response.data

def test_post_toggle_state(client):
    """
    Testa o POST na rota principal e verifica se o estado alterna.
    Este teste é básico: apenas confirma se a requisição concluiu
    e se a página continua acessível.
    """
    # Primeiro GET: deve estar "Desligado"
    response = client.get("/")
    assert b"Desligado" in response.data

    # POST: alterna estado
    response = client.post("/")
    assert response.status_code == 200
    
    # Verifica agora se no HTML apareceu "Ligado"
    assert b"Ligado" in response.data

    # POST mais uma vez para alternar de volta
    response = client.post("/")
    assert response.status_code == 200
    assert b"Desligado" in response.data

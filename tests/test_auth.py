import uuid
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_registrar_usuario():
    email = f"teste-{uuid.uuid4()}@email.com"
    response = client.post("/auth/registrar", json={
        "nome": "Teste",
        "email": email,
        "senha": "123456"
    })
    assert response.status_code == 200
    assert "mensagem" in response.json()


def test_registrar_email_invalido():
    response = client.post("/auth/registrar", json={
        "nome": "Teste",
        "email": "emailinvalido",
        "senha": "123456"
    })
    assert response.status_code == 422


def test_login_credenciais_invalidas():
    response = client.post("/auth/login", json={
        "email": "naoexiste@email.com",
        "senha": "senhaerrada"
    })
    assert response.status_code == 400


def test_registrar_email_duplicado():
    email = f"duplicado-{uuid.uuid4()}@email.com"
    client.post("/auth/registrar", json={
        "nome": "Teste",
        "email": email,
        "senha": "123456"
    })
    response = client.post("/auth/registrar", json={
        "nome": "Teste",
        "email": email,
        "senha": "123456"
    })
    assert response.status_code == 400

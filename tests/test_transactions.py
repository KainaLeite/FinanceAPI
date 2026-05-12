from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_tipo_invalido_em_transacao_sem_autenticacao():
    response = client.post("/transaction/criar-transacao", json={
        "valor": 100.0,
        "tipo": "invalido",
        "categoria_id": 1,
        "conta_id": "alguma-id",
        "data": "2026-05-11"
    }, headers={"Authorization": "Bearer tokenfalso"})
    assert response.status_code == 401

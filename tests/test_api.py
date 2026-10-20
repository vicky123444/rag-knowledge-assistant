from fastapi.testclient import TestClient

from src.rag_app.main import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert "RAG Knowledge Assistant API" in response.json()["message"]


def test_upload_rejects_unsupported_file_type():
    response = client.post(
        "/documents/ingest",
        files={"file": ("notes.exe", b"not a supported file", "application/octet-stream")},
    )
    assert response.status_code == 400
    assert "Supported file types" in response.json()["detail"]

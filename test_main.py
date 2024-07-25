import pytest
from httpx import AsyncClient
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

@pytest.mark.asyncio
async def test_get_companies():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/api/companies")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

@pytest.mark.asyncio
async def test_get_company():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/api/companies/1")
    assert response.status_code == 200
    assert "company_id" in response.json()

@pytest.mark.asyncio
async def test_get_company_not_found():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/api/companies/9999")
    assert response.status_code == 404

@pytest.mark.asyncio
async def test_get_locations():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/api/companies/1/locations")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

@pytest.mark.asyncio
async def test_healthcheck():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/api/healthcheck")
    assert response.status_code == 200
    assert response.json() == {'status': 'ok'}

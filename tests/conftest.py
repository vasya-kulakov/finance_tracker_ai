import pytest
from httpx import ASGITransport, AsyncClient
from src.docs.docs import Docs
from run import app
from src.db.database import engine


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"

@pytest.fixture(autouse=True)
async def clean_app_state():
    yield
    app.dependency_overrides.clear()


@pytest.fixture
async def ac():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://localhost:8000") as client:
        yield client

@pytest.fixture
async def admin_ac():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://localhost:8000") as client:
        # Perform login to get the token
        response = await client.post("/login", data=Docs.admin_token_default)
        assert response.status_code == 200
        token = response.json()["access_token"]
        client.headers.update({"Authorization": f"Bearer {token}"})
        yield client

@pytest.fixture(scope="session", autouse=True)
async def dispose_engine():
    yield
    await engine.dispose()
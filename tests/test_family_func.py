import pytest
from httpx import AsyncClient
from src.api.depends import oauth2_scheme
from src.docs.docs import Docs


@pytest.mark.anyio
async def test_connection_with_a_server(ac: AsyncClient):
    '''Initial test (просто тестик на работоспособность запуска приложения)'''
    response = await ac.get('/')
    assert response.status_code == 200


@pytest.mark.anyio
async def test_connection_with_a_server_404(ac: AsyncClient):
    '''Initial test (просто тестик на работоспособность запуска приложения)'''
    response = await ac.get('/nonexistent')
    assert response.status_code == 404

@pytest.mark.anyio
async def test_add_parent(ac: AsyncClient):
    '''Test adding a parent'''
    response = await ac.put('/family/add_parent', json=Docs.parent_docs_json_format)
    print("\n--- STATUS CODE ---", response.status_code)
    print("\n--- RESPONSE TEXT ---", response.text)
    print('\n-----JSON---------', response.json())# Показывает сырой ответ вместо падения
    assert response.status_code == 200
    data = response.json()
    assert data['parent']['name'] == "John"
    assert 'id' in data['parent']
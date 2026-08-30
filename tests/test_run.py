import pytest
from httpx import AsyncClient

@pytest.mark.anyio
async def test_connection_with_a_server(ac: AsyncClient):
    '''Initial test (просто тестик на работоспособность запуска приложения)'''
    response = await ac.get('/')
    assert response.status_code == 200

@pytest.mark.anyio
async def test_reset_db(ac: AsyncClient):
    '''Сброс базы данных'''
    await ac.post('/admin/reset')
    db_check = await ac.get('/family')
    
    res_json = db_check.json()
    correct_json = {
        "family": []
    }
    assert res_json == correct_json

@pytest.mark.anyio
async def test_add_parent(ac: AsyncClient):
    response = await ac.put(url='/family/add_parent', json={
        "name": "John",
        "last_name": "Doe",
        "password": "securepassword"
    })
    res_json = response.json()  # <-- без await
    correct_json = {
        "message": "Parent added successfully",
        "parent": {
                "id": 1,
                "name": "John",
                "last_name": "Doe",
                "role": "PARENT",
                "capital": 0,
                "parent_id": None
    }}
    assert res_json == correct_json

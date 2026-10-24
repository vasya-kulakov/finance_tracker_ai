from httpx import AsyncClient
import pytest


@pytest.mark.anyio
async def check_admin_exists(ac: AsyncClient):
    response = await ac.get('/family')
    res_json = response.json()
    assert any(member.get('role') == 'ADMIN' for member in res_json.get('family', []))
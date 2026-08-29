'''Тесты для апишки и их ответа'''
from fastapi.testclient import TestClient
from run import app 


test_client = TestClient(app)

def test_connection_with_a_server():
    '''Initial test (просто тестик на работоспособность запуска приложения)'''
    response = test_client.get('/')
    assert response.status_code == 200




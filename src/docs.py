#Я думаю, для чистоты кода лучше вынести ее в отдельный класс и файл, как тут и обращаться через import

class Docs:
    parent_docs_json_format = {
        "name": "John",
        "last_name": "Doe",
        "password": "securepassword"
    }
    child_docs_json_format = {
        "name": "Jane",
        "last_name": "Doe",
        "password": "securepassword",
        'parent_id': 1
    }

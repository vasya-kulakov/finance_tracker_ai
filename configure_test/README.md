Для запуска проекта нужно:
-Vs code
-Виртуальное окружение питона + **pip install -r requirments.txt**
-Постгресикуэль и pgadmin
В постгре создать:
finance_server: postgres:12345
    finance_db -> (зависит от) postgres

Вот такой вид файла .env в корне проекта:
'''
DB_HOST=localhost
DB_PORT=5432
DB_USER=postgres
DB_PASSWORD=12345
DB_NAME=finance_db
'''

Выполнить команду **uvicorn run:app --reload**

В С Е !
# Glossary gRPC service

## Setup
1. Создать виртуальное окружение и установить зависимости:
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Сгенерировать Python-stubs из proto (если ещё не сгенерировано):
```bash
python -m grpc_tools.protoc -I./proto --python_out=. --grpc_python_out=. ./proto/glossary.proto
```

3. Запустить сервер:
```bash
python app/server.py
```
Сервер слушает `localhost:50051`.

4. Запустить клиент:
```bash
python client.py
```

## Docker
Собрать образ и запустить:
```bash
docker build -t glossary-grpc .
docker run -p 50051:50051 glossary-grpc
```

## Примечания
- БД `glossary.db` будет создана в рабочей директории контейнера / локально. Для сохранения данных при запуске в Docker пробросьте volume.
- В этом примере используется простая авто-создание таблиц (`Base.metadata.create_all`) — если хочешь, добавим Alembic для миграций и автонкат при старте (как в REST-версии).

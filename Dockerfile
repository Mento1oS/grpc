FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Скомпилируем protobuf в контейнере (если не сгенерили локально)
RUN python -m grpc_tools.protoc -I./proto --python_out=. --grpc_python_out=. ./proto/glossary.proto

EXPOSE 50051

CMD ["python", "-u", "app/server.py"]

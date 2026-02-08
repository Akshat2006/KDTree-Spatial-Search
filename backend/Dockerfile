FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    gcc \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY c_core/ ./c_core/
WORKDIR /app/c_core/src
RUN gcc -o kdtree main.c kdtree.c -lm

WORKDIR /app

COPY python_api/requirements.txt ./python_api/
RUN pip install --no-cache-dir -r python_api/requirements.txt

COPY python_api/ ./python_api/

WORKDIR /app/python_api

EXPOSE 8000

CMD ["python", "main.py"]

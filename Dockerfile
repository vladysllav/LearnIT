FROM python:3.11-slim-buster

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-dev

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

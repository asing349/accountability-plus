FROM python:3.10-slim

WORKDIR /app
COPY . .
RUN pip install --upgrade pip && pip install fastapi uvicorn pydantic

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]

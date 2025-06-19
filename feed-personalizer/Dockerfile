FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .
COPY model.pkl .
COPY content_type_encoder.pkl .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]


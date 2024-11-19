FROM python:3.9-slim

WORKDIR /app

COPY src/requirements.txt .
COPY .env .

RUN pip install -r requirements.txt

COPY src/ .

EXPOSE 5001

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "5001"] 

FROM python:3.9-slim

WORKDIR /app

COPY src/requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5001

CMD ["sh", "-c", "cd src && python app.py"]

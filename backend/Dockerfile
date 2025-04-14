# FROM python:3.10
# WORKDIR /app
# COPY . .
# RUN pip install fastapi psycopg2-binary uvicorn
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
# backend/Dockerfile
FROM python:3.10

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Add wait-for-it script
COPY wait-for-it.sh /wait-for-it.sh
RUN chmod +x /wait-for-it.sh

CMD ["/wait-for-it.sh", "postgres:5432", "--", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]


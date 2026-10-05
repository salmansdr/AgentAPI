FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .
COPY order_service.py .
COPY customer_service.py .
COPY product_service.py .
COPY project_estimation.py .
COPY db.py .
COPY .env .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
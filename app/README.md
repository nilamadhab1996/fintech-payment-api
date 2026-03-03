# FinTech Payment API

This project is a simple payment backend service built using Flask and PostgreSQL.  
It simulates real-world fintech architectures used in companies like Razorpay and Zeta.

## Features
- Store payment transactions
- Health check endpoint
- REST API
- PostgreSQL database

## API Endpoints

### Health
GET /health

### Create Payment
POST /payment
{
  "user": "nil",
  "amount": 100
}

## Setup Locally

1. Install PostgreSQL
2. Create database:
createdb payments

3. Create table:
CREATE TABLE transactions (
  id SERIAL PRIMARY KEY,
  user_id VARCHAR(50),
  amount INT
);

4. Install dependencies:
pip install -r requirements.txt

5. Run:
python app.py

## Future Improvements
- Docker
- Redis
- Nginx
- Kubernetes
- CI/CD

## Author
Nilamadhab Purohit
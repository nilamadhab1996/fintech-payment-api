from flask import Flask, request, jsonify
import psycopg2
import redis
import os
import time
import logging

# ---------------------------
# Logging (Production style)
# ---------------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# ---------------------------
# Environment Variables
# ---------------------------
DB_HOST = os.getenv("DB_HOST", "db")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASS", "postgres")

# ---------------------------
# Database Connection with Retry
# ---------------------------
def get_conn():
    while True:
        try:
            conn = psycopg2.connect(
                host=DB_HOST,
                database="payments",
                user=DB_USER,
                password=DB_PASS
            )
            logger.info("Connected to DB")
            return conn
        except Exception as e:
            logger.error("DB not ready, retrying... %s", e)
            time.sleep(3)

# ---------------------------
# Auto DB Initialization
# ---------------------------
def init_db():
    logger.info("Initializing database...")
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id SERIAL PRIMARY KEY,
            user_id VARCHAR(50),
            amount INT
        )
    """)

    conn.commit()
    cur.close()
    conn.close()
    logger.info("DB ready")

# ---------------------------
# Redis Connection
# ---------------------------
def get_redis():
    while True:
        try:
            r = redis.Redis(host="redis", port=6379)
            r.ping()
            logger.info("Connected to Redis")
            return r
        except Exception as e:
            logger.error("Redis not ready, retrying... %s", e)
            time.sleep(2)

# ---------------------------
# Routes
# ---------------------------
@app.route("/")
def home():
    return {"message": "FinTech Payment API running"}

@app.route("/health")
def health():
    # DB check
    conn = get_conn()
    conn.close()

    # Redis check
    r = get_redis()
    r.set("health", "ok")

    return {"status": "healthy"}

@app.route("/payment", methods=["POST"])
def payment():
    data = request.json

    if not data or "user" not in data or "amount" not in data:
        return {"error": "Invalid payload"}, 400

    # Save to DB
    conn = get_conn()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO transactions (user_id, amount) VALUES (%s, %s)",
        (data["user"], data["amount"])
    )

    conn.commit()
    cur.close()
    conn.close()

    # Cache last payment in Redis
    r = get_redis()
    r.set("last_payment", data["amount"])

    logger.info("Payment stored for user %s", data["user"])

    return {"message": "Payment stored successfully"}

# ---------------------------
# Entry Point
# ---------------------------
if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=8000)
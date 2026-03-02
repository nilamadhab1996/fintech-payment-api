from flask import Flask, request, jsonify
import psycopg2

app = Flask(__name__)

def get_conn():
    return psycopg2.connect(
        host="localhost",
        database="payments",
        user="postgres",
        password="postgres"
    )

@app.route("/health")
def health():
    return {"status": "Payment API running"}

@app.route("/payment", methods=["POST"])
def payment():
    data = request.json
    conn = get_conn()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO transactions (user_id, amount) VALUES (%s, %s)",
        (data["user"], data["amount"])
    )

    conn.commit()
    cur.close()
    conn.close()

    return {"message": "Payment stored successfully"}

if __name__ == "__main__":
    app.run(debug=True)
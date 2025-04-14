# ==========================
# 🚀 BACKEND (FastAPI main.py)
# ==========================
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
import psycopg2
from psycopg2.extras import RealDictCursor
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

try:
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST", "postgres"),
        dbname=os.getenv("DB_NAME", "transactions"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASS", "password")
    )
    cur = conn.cursor(cursor_factory=RealDictCursor)
    print("✅ Connected to PostgreSQL")
except Exception as e:
    print("❌ Could not connect to PostgreSQL:", e)
    raise

@app.get("/transactions")
def list_transactions(
    search: str = Query("", alias="search"),
    page: int = Query(1, gt=0),
    limit: int = Query(10, gt=0, le=100)
):
    offset = (page - 1) * limit
    query = f"""
        SELECT * FROM transactions
        WHERE transaction_id ILIKE %s OR from_user ILIKE %s OR to_merchant ILIKE %s
        ORDER BY timestamp DESC
        LIMIT %s OFFSET %s
    """
    like = f"%{search}%"
    cur.execute(query, (like, like, like, limit, offset))
    transactions = cur.fetchall()

    count_query = """
        SELECT COUNT(*) FROM transactions
        WHERE transaction_id ILIKE %s OR from_user ILIKE %s OR to_merchant ILIKE %s
    """
    cur.execute(count_query, (like, like, like))
    total = cur.fetchone()["count"]

    return {
        "transactions": transactions,
        "total_pages": (total + limit - 1) // limit
    }

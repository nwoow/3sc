from kafka import KafkaConsumer
from kafka.errors import NoBrokersAvailable
import psycopg2, json, time

# Kafka connection retry logic
def wait_for_kafka():
    for i in range(10):
        try:
            consumer = KafkaConsumer(
                "transactions",
                bootstrap_servers="kafka:9092",
                value_deserializer=lambda x: json.loads(x.decode("utf-8"))
            )
            print("✅ Kafka Consumer connected.")
            return consumer
        except NoBrokersAvailable:
            print(f"🕒 Kafka not available, retrying in 3s... ({i+1}/10)")
            time.sleep(3)
    print("❌ Kafka connection failed after retries.")
    exit(1)

consumer = wait_for_kafka()

# PostgreSQL connection
conn = psycopg2.connect(
    host="postgres",
    dbname="transactions",
    user="postgres",
    password="password"
)
cur = conn.cursor()

# Create table if not exists
cur.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        transaction_id VARCHAR PRIMARY KEY,
        from_user VARCHAR,
        to_merchant VARCHAR,
        timestamp TIMESTAMP,
        amount NUMERIC,
        currency VARCHAR,
        product_id VARCHAR,
        quantity INTEGER
    );
""")
conn.commit()

# Consume messages
for msg in consumer:
    d = msg.value
    try:
        cur.execute("""
            INSERT INTO transactions (
                transaction_id, from_user, to_merchant, timestamp,
                amount, currency, product_id, quantity
            ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
            ON CONFLICT (transaction_id) DO NOTHING;
        """, (
            d["transaction_id"], d["from_user"], d["to_merchant"], d["timestamp"],
            d["amount"], d["currency"], d["product_id"], d["quantity"]
        ))
        conn.commit()
        print("✅ Inserted:", d["transaction_id"])
    except Exception as e:
        print("❌ DB Insert Error:", e)

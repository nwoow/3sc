from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable
from faker import Faker
import uuid, random, time, json
from datetime import datetime

fake = Faker()

# Kafka connection retry logic
def wait_for_kafka():
    for i in range(1000):
        try:
            producer = KafkaProducer(
                bootstrap_servers='kafka:9092',
                value_serializer=lambda x: json.dumps(x).encode('utf-8')
            )
            print("✅ Kafka Producer connected.")
            return producer
        except NoBrokersAvailable:
            print(f"🕒 Kafka not available, retrying in 3s... ({i+1}/10)")
            time.sleep(3)
    print("❌ Kafka connection failed after retries.")
    exit(1)

producer = wait_for_kafka()

def generate_transaction():
    return {
        "transaction_id": str(uuid.uuid4()),
        "from_user": fake.user_name(),
        "to_merchant": fake.company(),
        "timestamp": datetime.utcnow().isoformat(),
        "amount": round(random.uniform(5, 500), 2),
        "currency": "USD",
        "product_id": f"P{random.randint(1000,9999)}",
        "quantity": random.randint(1, 10)
    }

# Send 17 txns per second ~ 1000/minute
while True:
    for _ in range(17):
        txn = generate_transaction()
        try:
            producer.send("transactions", txn)
            print("📤 Sent:", txn["transaction_id"])
        except Exception as e:
            print("❌ Failed to send transaction:", e)
    time.sleep(1)

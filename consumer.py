from kafka import KafkaConsumer
import json

def safe_deserialize(value):
    if not value:
        return None
    try:
        return json.loads(value.decode("utf-8"))
    except Exception:
        return None

consumer = KafkaConsumer(
    "server_metrics",
    bootstrap_servers="localhost:9092",
    auto_offset_reset="earliest",
    enable_auto_commit=True,
    group_id="aiops-monitor-v2",  # Updated group ID to process cleanly
    value_deserializer=safe_deserialize
)

print("Waiting for messages...")

for message in consumer:
    data = message.value

    # Skip invalid or empty messages
    if not data or not isinstance(data, dict):
        continue

    server = data.get("server_id", "Unknown")
    cpu = data.get("cpu_usage", 0)
    memory = data.get("memory_usage", 0)

    print("\nReceived:")
    print("Server:", server)
    print("CPU:", cpu, "%")
    print("Memory:", memory, "%")

    if cpu > 80:
        print("ALERT: High CPU detected on", server)
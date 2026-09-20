from kafka import KafkaConsumer
import json

# Safe JSON deserializer function
def safe_deserialize(value):
    if not value:
        return None
    try:
        return json.loads(value.decode("utf-8"))
    except Exception:
        return None

# Initialize Consumer for 'server_metrics' topic
consumer = KafkaConsumer(
    "server_metrics",
    bootstrap_servers="localhost:9092",
    auto_offset_reset="earliest",  # Read topic from beginning
    enable_auto_commit=True,
    group_id="aiops-integrated-monitor",
    value_deserializer=safe_deserialize
)

print("Starting Integrated AIOps Monitoring System...\n")

anomaly_count = 0

try:
    for message in consumer:
        data = message.value

        # Skip invalid/empty payloads
        if not data or not isinstance(data, dict):
            continue

        server = data.get("server_id", "Unknown")
        cpu = data.get("cpu_usage", 0)

        # Real-time monitoring & stateful anomaly counter
        if cpu > 80:
            anomaly_count += 1
            print(f"Message received: {server} | CPU: {cpu}%")
            print("ALERT: High CPU detected\n")
        else:
            print(f"Message received: {server} | CPU: {cpu}%")
            print("Normal\n")

except KeyboardInterrupt:
    print("\nStopping monitoring system...")

finally:
    # Print final summary report upon shutdown
    print("===============================")
    print(f"Total anomalies detected: {anomaly_count}")
    print("===============================")
    consumer.close()
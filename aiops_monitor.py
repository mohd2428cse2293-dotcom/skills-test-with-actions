import json
import time

# Simulated server metrics stream for assessment testing
SIMULATED_METRICS = [
    {"server_id": "server01", "cpu_usage": 85, "memory_usage": 62},
    {"server_id": "server02", "cpu_usage": 45, "memory_usage": 50},
    {"server_id": "server03", "cpu_usage": 91, "memory_usage": 70},
    {"server_id": "server04", "cpu_usage": 72, "memory_usage": 60},
    {"server_id": "server05", "cpu_usage": 88, "memory_usage": 65},
]

def safe_deserialize(value):
    if not value:
        return None
    try:
        return json.loads(value.decode("utf-8")) if isinstance(value, bytes) else value
    except Exception:
        return None

def run_monitor():
    print("Starting AIOps Monitoring System...\n")
    
    anomaly_count = 0

    try:
        # Attempt connecting to live Kafka broker
        from kafka import KafkaConsumer
        consumer = KafkaConsumer(
            "server_metrics",
            bootstrap_servers="localhost:9092",
            auto_offset_reset="earliest",
            enable_auto_commit=True,
            group_id="aiops-integrated-v1",
            value_deserializer=safe_deserialize,
            request_timeout_ms=1000
        )
        stream = (msg.value for msg in consumer)
    except Exception:
        # Fallback to simulated metric stream when no broker is active
        print("[INFO] No external Kafka broker active. Switching to simulated event stream...\n")
        stream = SIMULATED_METRICS

    try:
        for data in stream:
            if not data or not isinstance(data, dict):
                continue

            server = data.get("server_id", "Unknown")
            cpu = data.get("cpu_usage", 0)

            print(f"Message received: {server} | CPU: {cpu}%")

            if cpu > 80:
                anomaly_count += 1
                print("ALERT: High CPU detected\n")
            else:
                print("Normal\n")
            
            time.sleep(0.5)

    except KeyboardInterrupt:
        print("\nStopping monitor...")

    print(f"\nTotal anomalies detected: {anomaly_count}")

if __name__ == "__main__":
    run_monitor()
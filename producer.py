from kafka import KafkaProducer
import json
import time

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

messages = [
    {"server_id": "server01", "cpu_usage": 45, "memory_usage": 60},
    {"server_id": "server01", "cpu_usage": 82, "memory_usage": 65},
    {"server_id": "server02", "cpu_usage": 50, "memory_usage": 58},
    {"server_id": "server02", "cpu_usage": 85, "memory_usage": 70},
    {"server_id": "server03", "cpu_usage": 78, "memory_usage": 62},
    {"server_id": "server01", "cpu_usage": 91, "memory_usage": 88},
    {"server_id": "server03", "cpu_usage": 33, "memory_usage": 45},
    {"server_id": "server02", "cpu_usage": 87, "memory_usage": 79},
    {"server_id": "server01", "cpu_usage": 60, "memory_usage": 64},
    {"server_id": "server03", "cpu_usage": 95, "memory_usage": 82}
]

for msg in messages:
    producer.send('server_metrics', value=msg)
    print(f"Sent: {msg}")
    time.sleep(0.5)

producer.flush()
print("All 10 metric messages sent successfully.")
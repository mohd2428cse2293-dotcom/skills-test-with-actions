import json
import time

def process_metric(data):
    """Parses metric dictionary, prints details, and checks for high CPU alerts."""
    server = data.get("Server") or data.get("server") or "unknown"
    cpu_str = str(data.get("CPU") or data.get("cpu", "0")).replace("%", "")
    memory = data.get("Memory") or data.get("memory", "N/A")
    
    try:
        cpu_val = float(cpu_str)
    except ValueError:
        cpu_val = 0.0

    # Format output as requested
    print(f"Received:\nServer: {server}\nCPU: {int(cpu_val)}%\nMemory: {memory}\n")

    # Alert condition: CPU > 80%
    if cpu_val > 80:
        print(f"ALERT: High CPU detected on {server}\n")


def run_kafka_consumer():
    topic_name = "server_metrics"
    
    try:
        from kafka import KafkaConsumer
        print(f"Connecting to Kafka broker for topic '{topic_name}'...")
        consumer = KafkaConsumer(
            topic_name,
            bootstrap_servers=['localhost:9092'],
            auto_offset_reset='earliest',
            value_deserializer=lambda x: json.loads(x.decode('utf-8')),
            consumer_timeout_ms=5000
        )
        
        for message in consumer:
            process_metric(message.value)
            
    except Exception as e:
        print(f"[INFO] Kafka broker not available ({e}). Running simulated stream...\n")
        
        # Test stream matching Question 3 specifications
        simulated_metrics = [
            {"Server": "server01", "CPU": "85%", "Memory": "62%"},
            {"Server": "server02", "CPU": "45%", "Memory": "50%"},
            {"Server": "server03", "CPU": "91%", "Memory": "78%"},
        ]
        
        for metric in simulated_metrics:
            time.sleep(1)
            process_metric(metric)

if __name__ == "__main__":
    run_kafka_consumer()
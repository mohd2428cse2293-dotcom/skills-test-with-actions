from kafka.admin import KafkaAdminClient, NewTopic

def create_kafka_topic():
    admin_client = KafkaAdminClient(
        bootstrap_servers="localhost:9092",
        client_id='admin_client'
    )
    
    topic_list = [NewTopic(name="server_metrics", num_partitions=1, replication_factor=1)]
    
    try:
        admin_client.create_topics(new_topics=topic_list, validate_only=False)
        print("Topic 'server_metrics' created successfully.")
    except Exception as e:
        print(f"Topic creation status/error: {e}")

if __name__ == "__main__":
    create_kafka_topic()
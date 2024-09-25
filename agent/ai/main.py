from kafka_consumer import consumer
from anomaly_detection import detect_anomalies

# Start consuming and detecting anomalies
if __name__ == "__main__":
    print("Starting Kafka consumer...")
    for message in consumer:
        log_entry = message.value
        detect_anomalies(log_entry)

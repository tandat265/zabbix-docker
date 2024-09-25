import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest

# Sample data for training the anomaly detection model
# You can replace this with your actual log data preprocessing logic
def preprocess_data(log_entry):
    # Example of preprocessing: extracting relevant fields
    # Here we assume log_entry is a dictionary
    try:
        # Convert your log entry into a DataFrame or array
        # You may need to adjust this according to your log structure
        data = {
            'response_time': log_entry.get('response_time'),  # Example field
            'status_code': log_entry.get('status_code'),  # Example field
        }
        return pd.DataFrame([data])
    except Exception as e:
        print(f"Error in preprocessing: {e}")
        return None

# Train the model (you can replace this with a more sophisticated approach)
def train_model(training_data):
    # Initialize the Isolation Forest model
    model = IsolationForest(contamination=0.05)  # Adjust contamination as needed
    model.fit(training_data)
    return model

# Detect anomalies in a new log entry
def detect_anomalies(log_entry):
    processed_data = preprocess_data(log_entry)
    if processed_data is not None:
        # Use the trained model to predict anomalies
        # You should keep the model trained on a larger dataset
        if 'model' not in globals():
            global model
            model = train_model(pd.DataFrame(columns=['response_time', 'status_code']))  # Initial model training
        prediction = model.predict(processed_data)
        
        # Anomaly if prediction is -1
        if prediction[0] == -1:
            print(f"Anomaly detected: {log_entry}")

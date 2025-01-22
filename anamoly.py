import pandas as pd
import openai
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from tqdm import tqdm

# Load enhanced log data
enhanced_csv_path = "redis_log_enhanced.csv"
df = pd.read_csv(enhanced_csv_path)

# OpenAI API key (Replace 'your-api-key' with actual key)
openai.api_key = "your-api-key"

# Generate embeddings for log messages using OpenAI GPT model
def get_embedding(text):
    response = openai.Embedding.create(
        input=text,
        model="text-embedding-ada-002"
    )
    return response['data'][0]['embedding']

# Compute embeddings for all log messages
df["embedding"] = df["message"].apply(lambda x: get_embedding(x))

# Convert embeddings into a NumPy array
embeddings = np.vstack(df["embedding"].values)

# Normalize embeddings
scaler = StandardScaler()
embeddings_scaled = scaler.fit_transform(embeddings)

# Train Isolation Forest for anomaly detection
model = IsolationForest(contamination=0.05, random_state=42)
df["anomaly_score"] = model.fit_predict(embeddings_scaled)

# Mark anomalies (1 = normal, -1 = anomaly)
df["anomaly_flag"] = df["anomaly_score"].apply(lambda x: 1 if x == -1 else 0)

# Save results
df.to_csv("redis_log_with_anomalies.csv", index=False)

print("Anomaly detection complete. Results saved to 'redis_log_with_anomalies.csv'.")

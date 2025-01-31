import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset with anomaly flags
df = pd.read_csv("redis_log_with_anomalies.csv")

# Convert timestamp column to datetime format
df["timestamp"] = pd.to_datetime(df["timestamp"])

# Separate normal and anomaly logs
normal_logs = df[df["anomaly_flag"] == 0]
anomaly_logs = df[df["anomaly_flag"] == 1]

# Plot log messages over time, highlighting anomalies
plt.figure(figsize=(12, 6))
plt.scatter(normal_logs["timestamp"], normal_logs.index, label="Normal Logs", color="blue", alpha=0.5, s=10)
plt.scatter(anomaly_logs["timestamp"], anomaly_logs.index, label="Anomalies", color="red", alpha=0.8, s=20)
plt.xlabel("Timestamp")
plt.ylabel("Log Index")
plt.title("Anomaly Detection in Redis Logs")
plt.legend()
plt.xticks(rotation=45)
plt.grid()
plt.show()

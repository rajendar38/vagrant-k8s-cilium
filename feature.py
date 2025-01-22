import pandas as pd
import re

# File paths
csv_file_path = "redis_log.csv"
enhanced_csv_path = "redis_log_enhanced.csv"

# Load the cleaned log data
df = pd.read_csv(csv_file_path)

# Convert date and time into a single datetime column
df["timestamp"] = pd.to_datetime(df["date"] + " " + df["time"], format="%d %b %Y %H:%M:%S.%f")

# Define log levels based on message content
def categorize_log_level(message):
    if "WARNING" in message or "Failed" in message or "Error" in message:
        return "ERROR"
    elif "Ready to accept connections" in message or "Running mode" in message:
        return "INFO"
    elif "Configuration loaded" in message:
        return "CONFIG"
    else:
        return "GENERAL"

df["log_level"] = df["message"].apply(categorize_log_level)

# Identify event types based on message patterns
def extract_event_type(message):
    if "Redis is starting" in message:
        return "Startup"
    elif "User requested shutdown" in message or "Redis is now ready to exit" in message:
        return "Shutdown"
    elif "Warning" in message or "Could not create" in message or "Failed" in message:
        return "Error"
    elif "Configuration loaded" in message:
        return "Configuration"
    elif "Ready to accept connections" in message:
        return "Ready"
    return "Other"

df["event_type"] = df["message"].apply(extract_event_type)

# Add error flag (1 if it's an error message, 0 otherwise)
df["error_flag"] = df["log_level"].apply(lambda x: 1 if x == "ERROR" else 0)

# Count errors per session
df["error_count"] = df["error_flag"].cumsum()

# Save the enhanced dataset
df.to_csv(enhanced_csv_path, index=False)

print(f"Enhanced log data saved to {enhanced_csv_path}")

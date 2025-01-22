import pandas as pd
import re

# File paths
log_file_path = "./redis-server.log"
csv_file_path = "redis_log.csv"

# Define a regex pattern to parse the log entries
log_pattern = re.compile(r'(?P<pid>\d+):(?P<ptype>[CM]) (?P<date>\d{2} \w{3} \d{4}) (?P<time>\d{2}:\d{2}:\d{2}\.\d{3}) (?P<level>[*#]) (?P<message>.+)')

# List to store parsed log entries
log_entries = []

# Read and parse the log file
with open(log_file_path, "r") as file:
    for line in file:
        match = log_pattern.match(line.strip())
        if match:
            log_entries.append(match.groupdict())

# Create a DataFrame
df = pd.DataFrame(log_entries)

# Save to CSV
df.to_csv(csv_file_path, index=False)

print(f"Log data saved to {csv_file_path}")

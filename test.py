import pandas as pd
import re

# Read the log file
log_file_path = './logs/server.log'
with open(log_file_path, 'r') as file:
    logs = file.readlines()

# Function to parse log lines (example for Apache logs)
def parse_log_line(line):
    pattern = r'(?P<ip>\S+) \S+ \S+ \[(?P<time>.*?)\] "(?P<method>\S+) (?P<url>\S+) \S+" (?P<status>\d+) (?P<size>\S+)'
    match = re.match(pattern, line)
    if match:
        return match.groupdict()
    return None

# Parse logs
parsed_logs = [parse_log_line(line) for line in logs if parse_log_line(line)]
df_logs = pd.DataFrame(parsed_logs)

# Convert 'time' column to datetime
df_logs['time'] = pd.to_datetime(df_logs['time'], format='%d/%b/%Y:%H:%M:%S %z')

# Fill missing values in 'size' column
df_logs['size'] = df_logs['size'].replace('-', 0).astype(int)

# Save cleaned logs to a CSV file
df_logs.to_csv('./logs/cleaned_server_logs.csv', index=False)
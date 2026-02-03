import json
import itertools
from datetime import datetime, timedelta
from collections import Counter
import pandas as pd


with open('logs.json', 'r') as file:
    logs = json.load(file)

log_levels = []
filtered_logs_error = filter(lambda log: log['level'] == 'ERROR', logs)
filtered_logs_warning =filter(lambda log: log['level'] == 'WARN', logs)
filtered_logs_info = filter(lambda log: log['level'] == 'INFO', logs)
filtered_logs_debug = filter(lambda log: log['level'] == 'DEBUG', logs)
filtered_logs_critical = filter(lambda log: log['level'] == 'CRITICAL', logs)

counts = {
    'ERROR': len(list(filtered_logs_error)),
    'WARN': len(list(filtered_logs_warning)),
    'INFO': len(list(filtered_logs_info)),
    'DEBUG': len(list(filtered_logs_debug)),
    'CRITICAL': len(list(filtered_logs_critical))
}
print("Log level counts:", counts)

# most active users
users = [entry["user_id"] for entry in logs if "user_id" in entry]
print("Users found in logs:", users)
user_counts = Counter(users)
most_active_users = max(user_counts, key=user_counts.get)
print("most active users:", most_active_users)


# error by hour
# error_by_hour = filter(lambda log: log['timestamp']=timedelta(hours=1), logs)

        

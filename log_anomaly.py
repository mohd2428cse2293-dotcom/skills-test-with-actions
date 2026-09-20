import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 1. Create Sample Dataset (20 records)
data = {
    'Timestamp': [f"10:{i:02d}" for i in range(20)],
    'CPU': [45, 50, 52, 48, 55, 95, 51, 49, 53, 50, 52, 97, 48, 51, 50, 54, 52, 92, 50, 49],
    'Memory': [60, 62, 61, 63, 65, 88, 62, 60, 61, 63, 64, 90, 61, 62, 63, 65, 62, 85, 61, 60],
    'Response_Time': [200, 210, 205, 198, 220, 450, 202, 200, 215, 208, 210, 480, 201, 205, 210, 218, 205, 460, 208, 200]
}

df = pd.DataFrame(data)

# 2. Detect Anomalies (Threshold: CPU > 80%)
anomalies = df[df['CPU'] > 80]

# 3. Print Expected Console Summary
print(f"Total records: {len(df)}")
print(f"Anomalies detected: {len(anomalies)}\n")
print(f"{'Timestamp':<15} {'CPU':<10} {'Status':<10}")

for _, row in anomalies.iterrows():
    print(f"{row['Timestamp']:<15} {row['CPU']}%{'':<6} ANOMALY")

# 4. Display Graph
plt.figure(figsize=(10, 5))
plt.plot(df['Timestamp'], df['CPU'], label='CPU Usage (%)', color='blue', marker='o')
plt.scatter(anomalies['Timestamp'], anomalies['CPU'], color='red', s=100, label='Anomaly', zorder=5)
plt.axhline(y=80, color='r', linestyle='--', label='CPU Threshold (80%)')
plt.title('AIOps Log Anomaly Detection - CPU Metrics')
plt.xlabel('Timestamp')
plt.ylabel('CPU Usage (%)')
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()
plt.show()
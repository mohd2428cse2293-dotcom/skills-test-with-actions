import pandas as pd
import matplotlib.pyplot as plt

# 1. Dataset generation (20 records)
data = {
    'Timestamp': [
        '10:00', '10:01', '10:02', '10:03', '10:04', '10:05', '10:06', '10:07', '10:08', '10:09',
        '10:10', '10:11', '10:12', '10:13', '10:14', '10:15', '10:16', '10:17', '10:18', '10:19'
    ],
    'CPU': [45, 50, 52, 48, 55, 95, 60, 58, 62, 51, 53, 49, 97, 54, 56, 50, 52, 47, 92, 51],
    'Memory': [60, 62, 61, 63, 65, 88, 64, 62, 66, 61, 60, 59, 91, 62, 63, 61, 60, 58, 85, 60],
    'Response_Time': [120, 125, 130, 118, 140, 450, 135, 128, 132, 121, 124, 119, 480, 126, 129, 122, 125, 115, 410, 120]
}

df = pd.DataFrame(data)

# 2. Statistics calculation
print("=== Metric Statistics ===")
print(df[['CPU', 'Memory', 'Response_Time']].describe())
print("\n")

# 3. Anomaly Detection (CPU > 80 threshold)
anomalies = df[df['CPU'] > 80]

# 4. Formatted Console Output
print(f"Total records: {len(df)}")
print(f"Anomalies detected: {len(anomalies)}\n")
print(f"{'Timestamp':<15} {'CPU':<10} {'Status'}")

for _, row in anomalies.iterrows():
    print(f"{row['Timestamp']:<15} {row['CPU']}%{'':<6} ANOMALY")

# 5. Visualization
plt.figure(figsize=(10, 5))
plt.plot(df['Timestamp'], df['CPU'], marker='o', label='CPU Usage (%)', color='blue')
plt.axhline(y=80, color='red', linestyle='--', label='Anomaly Threshold (80%)')

# Plot anomaly markers
plt.scatter(anomalies['Timestamp'], anomalies['CPU'], color='red', s=100, zorder=5, label='Anomaly')

plt.title('Server CPU Usage & Anomaly Detection')
plt.xlabel('Timestamp')
plt.ylabel('CPU Usage (%)')
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()
plt.show()
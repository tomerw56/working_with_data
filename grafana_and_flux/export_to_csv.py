from influxdb_client import InfluxDBClient
import pandas as pd

client = InfluxDBClient(
    url="http://localhost:8086",
    token="demo-token",
    org="demo-org"
)

query = """
from(bucket: "drone")
  |> range(start: -24h)
  |> filter(fn: (r) => r._measurement == "drone_telemetry")
  |> filter(fn: (r) => r._field == "alt")
"""

df = client.query_api().query_data_frame(query)

# Clean up for Orange
df = df[["_time", "drone_id", "_value"]]
df.columns = ["time", "drone_id", "altitude"]

df.to_csv("drone_altitude.csv", index=False)
print("Exported drone_altitude.csv")

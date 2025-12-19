from influxdb_client import InfluxDBClient

client = InfluxDBClient(
    url="http://localhost:8086",
    token="demo-token",
    org="demo-org"
)

query = """
from(bucket: "drone")
  |> range(start: -1h)
  |> filter(fn: (r) => r._measurement == "drone_telemetry")
"""

df = client.query_api().query_data_frame(query)
print(df[0].head())

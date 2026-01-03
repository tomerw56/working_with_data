from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import time


org = "demo-org"
url = "http://localhost:8086"
token="v7XOrg5XTxuax_EF51rttsVFeNMbSet6PuFGzS2Ywrae9aOegghd1tJaQlyZvC_UIEIWxS6KktwNUHUY4c54kg=="
client = InfluxDBClient(url=url, token=token, org=org)

write_api = client.write_api(write_options=SYNCHRONOUS)

bucket="metrics"

write_api = client.write_api(write_options=SYNCHRONOUS)
   
for value in range(5):
  point = (
    Point("measurement1")
    .tag("tagname1", "tagvalue1")
    .field("field1", value)
  )
  write_api.write(bucket=bucket, org="demo-org", record=point)
  time.sleep(1) # separate points by 1 second


query_api = client.query_api()

query = """from(bucket: "metrics")
 |> range(start: -10m)
 |> filter(fn: (r) => r._measurement == "measurement1")"""
tables = query_api.query(query, org="demo-org")

for table in tables:
  for record in table.records:
    print(record)

query_api = client.query_api()

query = """from(bucket: "metrics")
  |> range(start: -10m)
  |> filter(fn: (r) => r._measurement == "measurement1")
  |> mean()"""
tables = query_api.query(query, org="demo-org")

for table in tables:
    for record in table.records:
        print(record)

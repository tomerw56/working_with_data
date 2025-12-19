import time
import random
from datetime import datetime, timezone

import numpy as np
from influxdb_client import InfluxDBClient, Point, WritePrecision

INFLUX_URL = "http://localhost:8086"
TOKEN = "demo-token"
ORG = "demo-org"
BUCKET = "drone"

client = InfluxDBClient(url=INFLUX_URL, token=TOKEN, org=ORG)
write_api = client.write_api(write_precision=WritePrecision.NS)

def generate_drone_point(drone_id: int):
    lat = 32.0 + random.uniform(-0.01, 0.01)
    lon = 34.8 + random.uniform(-0.01, 0.01)
    alt = random.uniform(50, 120)

    vx, vy, vz = np.random.normal(0, 5, size=3)

    next_wp = random.randint(1, 20)
    dt_next = random.uniform(0.5, 5.0)

    p = (
        Point("drone_telemetry")
        .tag("drone_id", f"drone_{drone_id}")
        .field("lat", lat)
        .field("lon", lon)
        .field("alt", alt)
        .field("vx", vx)
        .field("vy", vy)
        .field("vz", vz)
        .field("next_wp", next_wp)
        .field("dt_next", dt_next)
        .time(datetime.now(timezone.utc))
    )

    return p

if __name__ == "__main__":
    print("Starting drone telemetry stream...")
    while True:
        points = [generate_drone_point(i) for i in range(3)]
        write_api.write(bucket=BUCKET, record=points)
        time.sleep(1)

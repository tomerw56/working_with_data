from drone_pb2 import DroneTelemetry

d = DroneTelemetry()
with open("drone.pb", "rb") as f:
    d.ParseFromString(f.read())

print({
    "drone_id": d.drone_id,
    "lat": d.lat,
    "lon": d.lon,
    "alt": d.alt,
    "vx": d.vx,
    "vy": d.vy,
    "vz": d.vz,
})

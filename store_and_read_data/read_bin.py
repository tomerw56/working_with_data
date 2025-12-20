import struct

fmt = "<Idddfff"  # little-endian
with open("drone.bin", "rb") as f:
    data = struct.unpack(fmt, f.read())

print({
    "drone_id": data[0],
    "lat": data[1],
    "lon": data[2],
    "alt": data[3],
    "vx": data[4],
    "vy": data[5],
    "vz": data[6],
})

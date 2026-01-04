import json
import pandas as pd
import boto3
from io import BytesIO, StringIO
from datetime import datetime
import random

# --- MinIO (S3-compatible) config ---
s3 = boto3.client(
    "s3",
    endpoint_url="http://localhost:9000",
    aws_access_key_id="minio",
    aws_secret_access_key="minio123",
)

BUCKET = "lake"

# --- Generate CSV data ---
csv_data = pd.DataFrame({
    "user_id": range(1, 11),
    "country": random.choices(["US", "DE", "IL"], k=10),
    "value": [random.randint(10, 100) for _ in range(10)],
    "ts": [datetime.utcnow().isoformat()] * 10
})

csv_buffer = StringIO()
csv_data.to_csv(csv_buffer, index=False)

s3.put_object(
    Bucket=BUCKET,
    Key="csv/events.csv",
    Body=csv_buffer.getvalue()
)

# --- Generate JSON data ---
json_events = [
    {
        "user_id": random.randint(1, 10),
        "event": random.choice(["login", "purchase", "logout"]),
        "amount": random.choice([None, random.randint(5, 50)]),
        "ts": datetime.utcnow().isoformat()
    }
    for _ in range(20)
]

json_buffer = BytesIO(
    "\n".join(json.dumps(e) for e in json_events).encode()
)

s3.put_object(
    Bucket=BUCKET,
    Key="json/events.json",
    Body=json_buffer.getvalue()
)

print("✅ Data uploaded to MinIO data lake")

import logging
import random
import time

logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

while True:
    if random.random() < 0.2:
        logging.error("Payment failed")
    else:
        logging.info("Request processed successfully")

    time.sleep(1)

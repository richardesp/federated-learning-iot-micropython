import time
import random
import os
import logging
from paho.mqtt.client import Client

# Logging configuration
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger()

# MQTT Broker configuration
BROKER = os.getenv("BROKER", "mosquitto")  # Container name for the broker
PORT = 1883
TOPIC = "iot/sensor_data"

# Function to simulate sensor data
def read_temperature():
    return round(random.uniform(20.0, 35.0), 2)

# Function to publish data
def publish_temperature(client):
    temperature = read_temperature()
    payload = f"{{'temperature': {temperature}}}"
    result = client.publish(TOPIC, payload)
    if result.rc == 0:
        logger.info(f"Published: {payload}")
    else:
        logger.error(f"Failed to publish: {payload}")

# MQTT client configuration
client = Client()

try:
    # Connect to the MQTT broker
    logger.info(f"Connecting to MQTT broker {BROKER}:{PORT}...")
    client.connect(BROKER, PORT, 60)

    # Publish data every 10 seconds
    while True:
        publish_temperature(client)
        time.sleep(10)

except KeyboardInterrupt:
    logger.info("Shutting down...")
    client.disconnect()

except Exception as e:
    logger.error(f"An error occurred: {e}")

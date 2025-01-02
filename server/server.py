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

# Callback function for received messages
def on_message(client, userdata, msg):
    payload = msg.payload.decode()
    logger.info(f"Message received on topic {msg.topic}: {payload}")

# MQTT client configuration
client = Client()
client.on_message = on_message

try:
    # Connect to the MQTT broker
    logger.info(f"Connecting to MQTT broker at {BROKER}:{PORT}...")
    client.connect(BROKER, PORT, 60)

    # Subscribe to the topic
    client.subscribe(TOPIC)
    logger.info(f"Subscribed to topic {TOPIC}. Waiting for messages...")

    # Keep the client running
    client.loop_forever()

except KeyboardInterrupt:
    logger.info("Shutting down...")
    client.disconnect()

except Exception as e:
    logger.error(f"An error occurred: {e}")

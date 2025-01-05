import os
import json
import paho.mqtt.client as mqtt
import logging

# Configuración de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("Server")

# Configuración MQTT
BROKER = os.getenv("BROKER", "localhost")
TOPIC_RECEIVE = "fl/+/params"
TOPIC_SEND = "fl/global_model"

# Almacén para los parámetros locales
local_params = []

# Callback para recibir parámetros locales
def on_message(client, userdata, message):
    global local_params
    try:
        payload = json.loads(message.payload.decode())
        logger.info(f"Parámetros recibidos: {payload}")
        local_params.append(payload["params"])
    except Exception as e:
        logger.error(f"Error al procesar mensaje: {e}")

# Agregación de parámetros locales
def aggregate():
    global local_params
    if local_params:
        try:
            global_model = sum(local_params) / len(local_params)  # Promedio simple
            logger.info(f"Modelo global actualizado: {global_model}")
            client.publish(TOPIC_SEND, json.dumps(global_model))
            local_params.clear()
        except Exception as e:
            logger.error(f"Error durante la agregación: {e}")

# Configuración del cliente MQTT
client = mqtt.Client("server")
client.on_message = on_message
client.connect(BROKER, 1883, 60)
client.loop_start()
client.subscribe(TOPIC_RECEIVE)

try:
    while True:
        aggregate()
except KeyboardInterrupt:
    logger.info("Servidor detenido por el usuario.")
    client.loop_stop()
    client.disconnect()

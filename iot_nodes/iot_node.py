import os
import json
import random
import socket
import paho.mqtt.client as mqtt
import logging
import time

# Configuración de logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("Node")

# Configuración del nodo
BROKER = os.getenv("BROKER", "localhost")
NODE_ID = os.getenv("NODE_ID", "node1")
TOPIC_SEND = f"fl/{NODE_ID}/params"
TOPIC_RECEIVE = "fl/global_model"
TOPIC_COMMAND = f"iot/{NODE_ID}/command"
TOPIC_CONTROL = "iot/control"

# Configuración de I2C simulado
I2C_HOST = os.getenv("IC2_HOST", "localhost")
I2C_PORT = 4000

# Simula un sensor de temperatura (lectura por I2C)
def get_sensor_data_i2c():
    logger.debug(f"[{NODE_ID}] Intentando leer datos del sensor I2C...")
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(b"READ", (I2C_HOST, I2C_PORT))
        data, _ = sock.recvfrom(1024)
        temperature = float(data.decode())
        logger.info(f"[{NODE_ID}] Temperatura leída (I2C): {temperature}")
        return temperature
    except Exception as e:
        logger.error(f"[{NODE_ID}] Error al leer datos del sensor: {e}")
        return random.uniform(20.0, 30.0)  # Valor por defecto en caso de error

# Simula el control de un actuador (LED)
def control_actuator(command):
    logger.debug(f"[{NODE_ID}] Ejecutando comando: {command}")
    if command == "turn_on":
        logger.info(f"[{NODE_ID}] Encendiendo LED")
    elif command == "turn_off":
        logger.info(f"[{NODE_ID}] Apagando LED")
    else:
        logger.warning(f"[{NODE_ID}] Comando desconocido: {command}")

# Callback para recibir el modelo global y comandos
def on_message(client, userdata, message):
    logger.debug(f"[{NODE_ID}] Mensaje recibido en el tópico {message.topic}")
    topic = message.topic
    payload = message.payload.decode()
    logger.info(f"[{NODE_ID}] Payload recibido: {payload}")
    
    if topic == TOPIC_RECEIVE:
        try:
            global_model = json.loads(payload)
            logger.info(f"[{NODE_ID}] Modelo global recibido: {global_model}")
        except Exception as e:
            logger.error(f"[{NODE_ID}] Error al procesar modelo global: {e}")
    elif topic == TOPIC_COMMAND:
        control_actuator(payload)

# Configuración del cliente MQTT
logger.info(f"[{NODE_ID}] Configurando cliente MQTT...")
client = mqtt.Client(NODE_ID)
client.on_message = on_message
try:
    client.connect(BROKER, 1883, 60)
    logger.info(f"[{NODE_ID}] Conectado al broker MQTT en {BROKER}:1883")
except Exception as e:
    logger.error(f"[{NODE_ID}] Error al conectar con el broker MQTT: {e}")
client.loop_start()
logger.info(f"[{NODE_ID}] Suscribiéndose a tópicos...")
client.subscribe(TOPIC_RECEIVE)
client.subscribe(TOPIC_COMMAND)

# Entrenamiento local
def train_local_model(data):
    logger.debug(f"[{NODE_ID}] Entrenando modelo local con datos: {data}")
    try:
        model_params = sum(data) / len(data)
        logger.info(f"[{NODE_ID}] Parámetros locales generados: {model_params}")
        return model_params
    except Exception as e:
        logger.error(f"[{NODE_ID}] Error durante el entrenamiento local: {e}")
        return 0

# Publica comandos para controlar otro nodo
def publish_control_command(client, temperature):
    logger.debug(f"[{NODE_ID}] Decidiendo comando de control para la temperatura: {temperature}")
    target_node = "node2" if NODE_ID == "node1" else "node1"
    try:
        if temperature > 25:
            client.publish(f"iot/{target_node}/command", "turn_on")
            logger.info(f"[{NODE_ID}] Comando enviado a {target_node}: turn_on")
        else:
            client.publish(f"iot/{target_node}/command", "turn_off")
            logger.info(f"[{NODE_ID}] Comando enviado a {target_node}: turn_off")
    except Exception as e:
        logger.error(f"[{NODE_ID}] Error al publicar comando de control: {e}")

# Bucle principal
logger.info(f"[{NODE_ID}] Iniciando bucle principal...")
data_buffer = []
while True:
    try:
        # Leer datos del sensor
        temperature = get_sensor_data_i2c()
        data_buffer.append(temperature)

        # Controlar otro nodo
        publish_control_command(client, temperature)

        # Entrenar y enviar parámetros locales cada 10 muestras
        if len(data_buffer) >= 10:
            local_params = train_local_model(data_buffer)
            payload = {"node_id": NODE_ID, "params": local_params}
            client.publish(TOPIC_SEND, json.dumps(payload))
            logger.info(f"[{NODE_ID}] Parámetros locales enviados: {payload}")
            data_buffer = []

        time.sleep(5)

    except KeyboardInterrupt:
        logger.info(f"[{NODE_ID}] Nodo detenido por el usuario.")
        break
    except Exception as e:
        logger.error(f"[{NODE_ID}] Error en el bucle principal: {e}")

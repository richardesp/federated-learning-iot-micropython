import socket
import random
import logging

# Configuración de logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger("IC2")

HOST = "0.0.0.0"
PORT = 4000

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((HOST, PORT))

logger.info("Servidor I2C Simulado escuchando en el puerto 4000...")
while True:
    data, addr = sock.recvfrom(1024)
    if data == b"READ":
        temperature = random.uniform(20.0, 30.0)
        sock.sendto(str(temperature).encode(), addr)

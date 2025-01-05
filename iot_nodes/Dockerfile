FROM espressif/idf:release-v5.0

RUN apt-get update && apt-get install -y python3 python3-venv

RUN python3 -m venv /venv

RUN /venv/bin/pip install --no-cache-dir paho-mqtt==1.6.1 numpy==1.19.5

WORKDIR /app

COPY iot_node.py /app/iot_node.py
COPY sockets/ic2.py /app/ic2.py

CMD ["sh", "-c", "/venv/bin/python /app/ic2.py & /venv/bin/python /app/iot_node.py"]
FROM espressif/idf:release-v5.0

RUN apt-get update && apt-get install -y python3 python3-venv

RUN python3 -m venv /venv

RUN /venv/bin/pip install --no-cache-dir paho-mqtt

WORKDIR /app

COPY iot_node.py /app/iot_node.py

CMD ["/venv/bin/python", "/app/iot_node.py"]

# Usar una imagen base con soporte para QEMU y ESP32
FROM mluis/qemu-esp32:latest

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /project

# Montar el directorio local como volumen (esto se configura al ejecutar el contenedor)
COPY . /project

# Instalar herramientas adicionales si es necesario
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Exponer el puerto en caso de que sea necesario (por ejemplo, para depuración)
EXPOSE 3333

# Comando predeterminado para iniciar una shell interactiva
CMD ["tail", "-f", "/dev/null"]

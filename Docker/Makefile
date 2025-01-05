# Variables
DOCKER_COMPOSE = docker-compose
PYTHON = python3

# Ayuda
.PHONY: help
help:
	@echo "Comandos disponibles:"
	@echo "  make up       - Ejecutar el servidor I2C y levantar todos los servicios con Docker Compose"
	@echo "  make down     - Detener todos los servicios de Docker Compose"
	@echo "  make restart  - Reiniciar la simulación completa"
	@echo " make logs      - Mostrar los logs de ejecución de todo el sistema IoT"

# Levantar todo (Servidor I2C y servicios)
.PHONY: up
up:
	@echo "Levantando los servicios con Docker Compose..."
	$(DOCKER_COMPOSE) up -d --build

# Apagar todos los servicios
.PHONY: down
down:
	@echo "Deteniendo los servicios de Docker Compose..."
	$(DOCKER_COMPOSE) down

# Reiniciar todo
.PHONY: restart
restart: down up

# Mostrar logs
.PHONY: logs
logs: 
	$(DOCKER_COMPOSE) logs -f
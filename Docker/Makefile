# Default values
DOCKER_COMPOSE = docker-compose
NODE_SERVICE = iot_node
SERVER_SERVICE = server

# Deploy the server
.PHONY: server
server:
	@echo "Starting the server service..."
	ROLE=server $(DOCKER_COMPOSE) up --build -d server
	@echo "Server service is running."

# Deploy N IoT node services dynamically
.PHONY: nodes
nodes:
	@if [ -z "$(N)" ]; then \
		echo "Error: Specify the number of nodes to deploy using 'make nodes N=<number>'"; \
		exit 1; \
	fi
	@echo "Starting $(N) IoT node services..."
	ROLE=server $(DOCKER_COMPOSE) up --build -d --scale $(NODE_SERVICE)=$(N)
	@echo "$(N) IoT node services are running."
	
# Stop all services
.PHONY: stop
stop:
	@echo "Stopping all services..."
	$(DOCKER_COMPOSE) down
	@echo "All services have been stopped."

# Clean up (remove containers, networks, volumes, and images)
.PHONY: clean
clean:
	@echo "Cleaning up all Docker resources..."
	$(DOCKER_COMPOSE) down --rmi all --volumes --remove-orphans
	@echo "Cleanup complete."

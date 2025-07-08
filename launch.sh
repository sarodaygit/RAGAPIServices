#!/bin/bash

# Usage:
#   ./launch.sh start dev
#   ./launch.sh stop prod
#   ./launch.sh restart dev
#   ./launch.sh status prod

ACTION=$1
ENV=$2

if [[ "$ACTION" != "start" && "$ACTION" != "stop" && "$ACTION" != "restart" && "$ACTION" != "status" ]]; then
  echo "❌ Usage: $0 {start|stop|restart|status} {dev|prod}"
  exit 1
fi

if [[ "$ENV" != "dev" && "$ENV" != "prod" ]]; then
  echo "❌ Environment must be one of: dev or prod"
  exit 1
fi

COMPOSE_FILE="docker-compose.${ENV}.yml"
NETWORK_NAME="fastapi_mongo_net"

# Create the network if not exists
if ! docker network ls --format '{{.Name}}'
 | grep -wq "$NETWORK_NAME"; then
  echo "🔧 Docker network '$NETWORK_NAME' not found. Creating..."
  docker network create "$NETWORK_NAME"
  echo "✅ Network '$NETWORK_NAME' created."
else
  echo "🌐 Docker network '$NETWORK_NAME' already exists."
fi

# Ensure the compose file exists
if [[ ! -f "$COMPOSE_FILE" ]]; then
  echo "❌ Compose file $COMPOSE_FILE not found!"
  exit 1
fi

# Action logic
case "$ACTION" in
  start)
    echo "🚀 Starting FastAPI containers for $ENV..."
    docker-compose -f "$COMPOSE_FILE" up -d --build
    echo "✅ $ENV environment started."
    ;;
  stop)
    echo "🛑 Stopping FastAPI containers for $ENV..."
    docker-compose -f "$COMPOSE_FILE" down
    echo "✅ $ENV environment stopped."
    ;;
  restart)
    echo "🔄 Restarting FastAPI containers for $ENV..."
    docker-compose -f "$COMPOSE_FILE" down
    docker-compose -f "$COMPOSE_FILE" up -d --build
    echo "✅ $ENV environment restarted."
    ;;
  status)
    echo "📦 Docker status for $ENV:"
    docker-compose -f "$COMPOSE_FILE" ps
    ;;
esac

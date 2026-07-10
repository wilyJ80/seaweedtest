#!/bin/bash

# Dev script
## Prepares dev env

echo "[INFO] Discarding previous containers..."
docker compose -f docker/compose-dev.yaml down --remove-orphans -v

echo "[INFO] Building project..."
docker compose -f docker/compose-dev.yaml build

echo "[INFO] Preparing services..."
docker compose -f docker/compose-dev.yaml up -d

echo "[INFO] Services healthy."

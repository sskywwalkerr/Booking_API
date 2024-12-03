up: docker compose -f docker-compose-local.yaml up -d & docker compose up -d

down: docker compose -f docker-compose-local.yaml down && docker network prune --force
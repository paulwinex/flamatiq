include ./.env

up:
	docker-compose up -d

down:
	docker-compose down

build:
	docker-compose build

restart:
	make down
	make up

logs:
	docker-compose logs -f -n 1000

bash:
	docker exec -it ${APP_NAME}-app bash

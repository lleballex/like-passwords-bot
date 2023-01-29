include .env

build:
	docker build -t like-passwords-bot .
run:
	docker run -d --env-file .env --name like-passwords-bot -v ${PROJECT_PATH}/src/db:/app/src/db like-passwords-bot
run-dev:
	docker run -d --env-file .env --rm --name like-passwords-bot -v ${PROJECT_PATH}/src/db:/app/src/db like-passwords-bot

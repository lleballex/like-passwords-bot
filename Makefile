include .env

build:
	docker build -t like-passwords-bot .
run:
	docker run -d --name like-passwords-bot -v ${PROJECT_PATH}/src/db:/app/src/db like-passwords-bot
run-dev:
	docker run -d --rm --name like-passwords-bot -v ${PROJECT_PATH}/src/db:/app/src/db like-passwords-bot

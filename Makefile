#Makefile

.IGNORE: test

up:
	cp env/.env.prod .env.example
	docker-compose up

build:
	cp env/.env.prod .env.example
	docker-compose up --build

test:
	cp env/.env.test .env.example
	docker-compose --file docker-compose.test.yaml up --build

.DEFAULT_GOAL := test


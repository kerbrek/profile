.DEFAULT_GOAL := help

SHELL := /usr/bin/env bash

project := profile
app_dir := app

.PHONY: setup # Setup a working environment
setup:
	env PIPENV_VENV_IN_PROJECT=1 pipenv install --dev

.PHONY: shell # Spawn a shell within the virtual environment
shell:
	env PIPENV_DOTENV_LOCATION=.env.example pipenv shell

.PHONY: lint # Run linter
lint:
	pipenv run pylint ${app_dir}/ tests/

.PHONY: prepare-test-containers
prepare-test-containers:
	@echo Starting db container...
	@docker run -d \
		--rm \
		--pull missing \
		--name ${project}_test_db \
		--tmpfs /var/lib/postgresql/data \
		--env-file ./.env.example \
		-p 5433:5432 \
		postgres:13-alpine

stop-prepared-test-containers := echo; \
	echo Stopping db container...; \
	docker stop ${project}_test_db

.PHONY: test # Run tests
test: prepare-test-containers
	@sleep 1
	@trap '${stop-prepared-test-containers}' EXIT && \
		echo Starting tests... && \
		env PIPENV_DOTENV_LOCATION=.env.example \
			pipenv run env POSTGRES_PORT=5433 \
			pytest --verbosity=$(or $(v), 0) tests/

.PHONY: coverage # Run tests with coverage report
coverage: prepare-test-containers
	@sleep 1
	@trap '${stop-prepared-test-containers}' EXIT && \
		echo Starting tests... && \
		env PIPENV_DOTENV_LOCATION=.env.example \
			pipenv run env POSTGRES_PORT=5433 \
			pytest --cov-report term-missing:skip-covered --cov=${app_dir} tests/

.PHONY: prepare-temp-containers
prepare-temp-containers:
	@echo Starting db container...
	@docker run -d \
		--rm \
		--pull always \
		--name ${project}_temp_db \
		--env-file ./.env.example \
		-p 5432:5432 \
		postgres:13-alpine

stop-prepared-temp-containers := echo; \
	echo Stopping db container...; \
	docker stop ${project}_temp_db

.PHONY: start # Start development Web server
start: prepare-temp-containers
	@sleep 1
	@trap '${stop-prepared-temp-containers}' EXIT && \
		echo Initializing database... && \
		env PIPENV_DOTENV_LOCATION=.env.example \
			pipenv run python -m ${app_dir}.init_db && \
		echo Starting application... && \
		env PIPENV_DOTENV_LOCATION=.env.example \
			pipenv run uvicorn ${app_dir}.main:app --reload

.PHONY: alembic-revision # Create Alembic migration script
alembic-revision: prepare-temp-containers
	@sleep 1
	@trap '${stop-prepared-temp-containers}' EXIT && \
		echo Migrating database... && \
		env PIPENV_DOTENV_LOCATION=.env.example \
			pipenv run alembic upgrade head && \
		echo Creating a migration script... && \
		env PIPENV_DOTENV_LOCATION=.env.example \
			pipenv run alembic revision --autogenerate -m "$(m)"

.PHONY: requirements # Generate requirements.txt file
requirements:
	pipenv lock --requirements > requirements.txt

.PHONY: up # Start Compose services
up:
	docker-compose -p ${project} -f docker/docker-compose.yml pull db nginx
	docker-compose -p ${project} -f docker/docker-compose.yml build --pull
	docker-compose -p ${project} -f docker/docker-compose.yml up

.PHONY: down # Stop Compose services
down:
	docker-compose -p ${project} -f docker/docker-compose.yml down

.PHONY: up-dev # Start Compose services (development)
up-dev:
	docker-compose -p ${project} -f docker/docker-compose.dev.yml pull db
	docker-compose -p ${project} -f docker/docker-compose.dev.yml build --pull
	docker-compose -p ${project} -f docker/docker-compose.dev.yml up

.PHONY: down-dev # Stop Compose services (development)
down-dev:
	docker-compose -p ${project} -f docker/docker-compose.dev.yml down

.PHONY: up-debug # Start Compose services (debug)
up-debug:
	docker-compose -p ${project} -f docker/docker-compose.debug.yml pull db
	docker-compose -p ${project} -f docker/docker-compose.debug.yml build --pull
	docker-compose -p ${project} -f docker/docker-compose.debug.yml up

.PHONY: down-debug # Stop Compose services (debug)
down-debug:
	docker-compose -p ${project} -f docker/docker-compose.debug.yml down

.PHONY: help # Print list of targets with descriptions
help:
	@echo; \
		for mk in $(MAKEFILE_LIST); do \
			echo \# $$mk; \
			grep '^.PHONY: .* #' $$mk \
			| sed 's/\.PHONY: \(.*\) # \(.*\)/\1	\2/' \
			| expand -t20; \
			echo; \
		done

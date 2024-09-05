pwd := $(shell pwd)

build:
	@docker build . -t scp-aislider-app:1.0.0 -f ./docker/Dockerfile

build-local:
	@docker build . -t scp-aislider-app:1.0.0-local -f ./docker/Dockerfile.local --build-arg MY_TEST=테스트

build-arm64:
	@docker buildx build . -t scp-aislider-app:1.0.0-arm64 -f ./docker/Dockerfile --platform=linux/arm64

build-dev:
	@docker buildx build . -t scp-aislider-app:1.0.0-dev -f ./docker/Dockerfile.dev --platform=linux/arm64 --build-arg MY_TEST=테스트

build-dev4:
	@docker build . -t scp-aislider-app:1.0.4-dev -f ./docker/Dockerfile.dev --build-arg MY_TEST=테스트4

ps:
	@docker-compose ps

up:
	@docker-compose -f docker-compose.yaml up -d

down:
	@docker-compose -f docker-compose.yaml down

logs:
	@docker-compose logs -f dockapi

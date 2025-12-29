.PHONY: build up down logs test shell clean

build:
	docker-compose build
up:
	docker-compose up -d
down:
	docker-compose down
logs:
	docker-compose logs -f
test:
	docker-compose exec whisper-api pytest tests/
shell:
	docker-compose exec whisper-api /bin/bash
clean:
	rm -rf app/__pycache__ tests/__pycache__
	docker-compose exec whisper-api rm -rf /tmp/whisper_uploads/*
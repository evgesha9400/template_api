.PHONY: run-local requirements build clean run-container swagger deploy diff

PROJECT_NAME=template_api

run-local:
	@PYTHONPATH=src uvicorn main:app --reload --port 8000

requirements:
	@poetry export -f requirements.txt --without-hashes > src/requirements.txt

build:
	@docker build -t $(PROJECT_NAME) .

clean:
	-@docker stop $(PROJECT_NAME) 2>/dev/null || true
	-@docker rm $(PROJECT_NAME) 2>/dev/null || true
	-@docker rmi $(PROJECT_NAME) 2>/dev/null || true

run-container: clean build
	@docker run --name $(PROJECT_NAME)  -p 8000:80 -d $(PROJECT_NAME):latest

swagger:
	@PYTHONPATH=src python3 swagger.py

deploy: requirements
	@cd deploy && cdk deploy

diff:
	@cd deploy && cdk diff
run:
	@PYTHONPATH=src uvicorn main:app --reload --port 8000

requirements:
	@poetry export -f requirements.txt --without-hashes > src/requirements.txt

swagger:
	@PYTHONPATH=src python3 swagger.py

deploy: requirements
	cd deploy && cdk deploy
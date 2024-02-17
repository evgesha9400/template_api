run:
	@PYTHONPATH=src uvicorn main:app --reload --port 8000

requirements:
	@poetry export -f requirements.txt --without-hashes > src/requirements.txt

export_swagger:
	@PYTHONPATH=src python3 update_swagger.py


# Use an official lightweight Python image.
# https://hub.docker.com/_/python
FROM python:3.9-slim
LABEL org.opencontainers.image.title="template_api"

# Set the working directory in the container
WORKDIR /app

# Install any dependencies
COPY src/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY src/ .

# Specify the command to run on container start
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
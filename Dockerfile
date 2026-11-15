FROM python:3.11-slim

WORKDIR /app

# Install system dependencies if needed
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Copy requirements or install packages directly
COPY requirements.txt . 2>/dev/null || true
RUN pip install --no-cache-dir boto3 flask gunicorn

# Copy application code
COPY . .

EXPOSE 8080

CMD ["python", "app.py"]

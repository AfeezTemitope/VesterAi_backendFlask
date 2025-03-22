# Use Python slim image
FROM python:3.9-slim

# Install system dependencies for psycopg2
RUN apt-get update && apt-get install -y libpq-dev gcc

# Set working directory
WORKDIR /app

# Copy application code
COPY . .

# Copy the .env file
COPY .env .env

#copy requirements.txt
COPY requirements.txt requirements.txt

# Upgrade pip and install dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Expose the Flask port
EXPOSE 5000

# Run the Flask app
CMD ["flask", "run", "--host=0.0.0.0"]

FROM python:3.9-alpine

# Set working directory
WORKDIR /app

# Copy requirements.txt
COPY requirements.txt .

# install dependencies
RUN pip install -r requirements.txt

# Copy .env file
COPY .env .

# Expose the Flask port
EXPOSE 5000

# Run the Flask app
CMD ["python", "app.py"]

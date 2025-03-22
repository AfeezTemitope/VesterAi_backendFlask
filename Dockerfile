# Use Python Alpine for a lightweight image
FROM python:3.9-alpine

# Set working directory inside the container
WORKDIR /app

# Install system dependencies for libraries like lxml and pillow
RUN apk add --no-cache build-base libxml2-dev libxslt-dev jpeg-dev zlib-dev

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Set environment variables for Flask
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Expose the port Flask runs on
EXPOSE 5000

# Run the Flask application
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]

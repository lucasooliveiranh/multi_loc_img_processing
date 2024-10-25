# ui-service/Dockerfile

# Use official Python image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy requirements.txt and install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose port 5001
EXPOSE 5005

# Run the Flask app with async support
CMD ["python", "app.py"]
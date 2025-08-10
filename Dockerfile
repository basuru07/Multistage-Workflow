# Use official Python runtime as base image
FROM python:3.12-slim

# Set working directory in container
WORKDIR /app

# Copy the Python application
COPY app.py .

# Expose port 8000
EXPOSE 8000

# Set environment variables
ENV PORT=8000
ENV ENVIRONMENT=production

# Run the application
CMD ["python", "app.py"]
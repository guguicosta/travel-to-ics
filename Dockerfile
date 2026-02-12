# Dockerfile for containerized deployment
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements-production.txt .
RUN pip install --no-cache-dir -r requirements-production.txt

# Copy application files
COPY web_app_production.py .
COPY travel_to_ics.py .
COPY templates templates/

# Create static directory
RUN mkdir -p static

# Expose port
EXPOSE 8080

# Set environment variables
ENV PORT=8080
ENV DEBUG=False
ENV PYTHONUNBUFFERED=1

# Run with gunicorn
CMD gunicorn -w 4 -b 0.0.0.0:$PORT web_app_production:app

FROM python:3.10-slim

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Create necessary directories if they don't exist
RUN mkdir -p static/images/charts

# Create placeholder images if they don't exist
RUN python create_images.py || echo "Image creation skipped"

# Expose port for the application
EXPOSE 8080

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PORT=8080

# Run with gunicorn for production
CMD gunicorn --bind 0.0.0.0:$PORT app:app

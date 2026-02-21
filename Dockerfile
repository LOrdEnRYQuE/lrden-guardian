# LRDEnE Guardian - Commercial Deployment
# ======================================

FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p uploads lrden_guardian/locales

# Set environment variables
ENV FLASK_APP=web_dashboard/app.py
ENV FLASK_ENV=production
ENV PYTHONUNBUFFERED=1

# Expose ports
EXPOSE 5001

# Healthcheck
HEALTHCHECK --interval=30s --timeout=3s \
  CMD curl -f http://localhost:5001/api-info || exit 1

# Start application
CMD ["python", "web_dashboard/app.py"]

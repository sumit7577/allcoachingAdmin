# Use an official Python runtime as a parent image
FROM python:3.13.5-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies required by psycopg2
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container
COPY requirements.txt /app/

# Install any dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application into the container
COPY . /app/

# Expose port 8000 for Django
EXPOSE 8000

# Install Gunicorn in the container
RUN pip install gunicorn


# Run the Django development server (you can change it for production later)
CMD ["gunicorn", "--workers", "3", "--timeout", "10000", "--worker-class", "gthread", "--threads", "3", "--bind", "0.0.0.0:8000", "allcoaching.wsgi:application"]

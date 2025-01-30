# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt /app/

# Install any dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application into the container
COPY . /app/

# Expose port 8000 for Django
EXPOSE 8000

# Set the environment variable for Django settings
ENV DJANGO_SETTINGS_MODULE=allcoaching.settings

# Run the Django development server (you can change it for production later)
CMD ["gunicorn", "allcoaching.wsgi:application", "--bind", "0.0.0.0:8000"]

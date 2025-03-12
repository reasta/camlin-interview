# Dockerfile for Python app
FROM python:3.12

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the Python application files into the container
COPY . /app

# Expose the port the app runs on
EXPOSE 8000

# Command to run the main application
CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]
FROM python:3.12

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . /app

ENV DB_NAME=camlin_db
ENV DB_USER=camlin
ENV DB_PASSWORD=camlin_password

EXPOSE 8000

# Command to run the main application
CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]
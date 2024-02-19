# Use an official Python runtime as a parent image
FROM python:3.9-slim

WORKDIR /trading

# Copy the current directory contents into the container at /usr/src/app
COPY . .

RUN pip3 install  -r requirements.txt
# Command to run the application
CMD ["python3", "./main.py"]
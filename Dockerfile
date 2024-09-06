# Use a base image with Python 3.10
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose the port and run the application
EXPOSE 5000
CMD ["flask", "run", "--host=0.0.0.0"]

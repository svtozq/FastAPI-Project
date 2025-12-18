# Base image: Official Python
FROM python:3.11-slim

# Define the working folder in the container
WORKDIR /app

# Copy the dependencies file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all the backend code into the container
COPY . .

# Expose the port used by FastAPI
EXPOSE 8000

# Launching FastAPI with Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

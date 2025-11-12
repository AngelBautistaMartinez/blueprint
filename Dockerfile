# Use a lightweight Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy dependency list first (for caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app
COPY . .

# Expose Flask port
EXPOSE 5000

# Run Flask in unbuffered mode so logs show immediately
ENV PYTHONUNBUFFERED=1

# Start the app
CMD ["python", "app.py"]

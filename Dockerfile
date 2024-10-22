# Base image of Python with OS Debian slim (meaning small one)
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the dependencies file to the working directory
ADD . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Command to run on container start
ENTRYPOINT ["sh", "-c", "
    # Wait for MySQL to be ready
    sleep 10;  # Wait for 10 seconds before checking
    python data_sql.py
    sleep 5;   # Wait for 5 seconds after data_sql.py before starting the app
    python app.py
"]

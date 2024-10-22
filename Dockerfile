# Base image of Python with OS Debian slim (meaning small one)
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the dependencies file to the working directory
ADD . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Command to run on container start
ENTRYPOINT sh -c "
    # Wait for MySQL to be ready
    for i in {1..10}; do
        if python data_sql.py; then
            break;
        else
            sleep $((i * 5));
        fi
    done;

    # Start the Flask app
    python app.py
"

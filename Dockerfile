# base image of python with OS debian slim (meaning small one)
FROM python:3.12-slim

# set the working directory in the container
WORKDIR /app

# copy the dependencies file to the working directory
ADD . /app

# install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# command to run on container start
ENTRYPOINT ["sh", "-c", "
    # Wait for MySQL to be ready
    echo 'Waiting for MySQL to be ready...'
    for i in {1..10}; do
        if python data_sql.py; then
            echo 'MySQL is ready!'
            break
        else
            echo 'MySQL not ready yet, retrying in $((i * 5)) seconds...'
            sleep $((i * 5))
        fi
    done;

    # Start the Flask app
    echo 'Starting the Flask app...'
    python app.py
"]

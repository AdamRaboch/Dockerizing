# base image of python with OS debian slim (meaning small one)
FROM python:3.12-slim

# set the working directory in the container
WORKDIR /app

# copy the dependencies file to the working directory
ADD . /app

# install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# command to run on container start
ENTRYPOINT sh -c "
    # Create or clear the log file
    echo '' > /tmp/app.log;

    # Wait for MySQL to be ready
    echo 'Waiting for MySQL to be ready...' >> /tmp/app.log;
    for i in {1..10}; do
        if python data_sql.py >> /tmp/app.log 2>&1; then
            echo 'MySQL is ready!' >> /tmp/app.log;
            break;
        else
            echo 'MySQL not ready yet, retrying in $((i * 5)) seconds...' >> /tmp/app.log;
            sleep $((i * 5));
        fi
    done;

    # Start the Flask app
    echo 'Starting the Flask app...' >> /tmp/app.log;
    python app.py >> /tmp/app.log 2>&1
"

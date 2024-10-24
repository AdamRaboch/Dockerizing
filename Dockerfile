# base image of python with OS debian slim (meaning small one)
FROM python:3.12-slim

# Install MySQL client
RUN apt-get update && apt-get install -y default-mysql-client && rm -rf /var/lib/apt/lists/*

# set the working directory in the container
WORKDIR /app

# copy the dependencies file to the working directory
ADD . /app

# install dependencies
RUN pip install -r requirements.txt

# command to run on container start
ENTRYPOINT ["sh", "-c", "sleep 30 && python data_sql.py"]

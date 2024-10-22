import os
import mysql.connector
import logging

# Configure logging
logging.basicConfig(filename='/tmp/db_test.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

db_host = os.getenv("MYSQL_HOST")
try:
    db = mysql.connector.connect(
        host=db_host,
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        port=os.getenv("MYSQL_PORT", 3306)
    )
    logging.info("Successfully connected to MySQL at %s:%s", db_host, os.getenv("MYSQL_PORT", 3306))
except mysql.connector.Error as err:
    logging.error("Error connecting to MySQL: %s", err)

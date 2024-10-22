import os
import mysql.connector
import logging

# Configure logging
logging.basicConfig(filename='/tmp/db_test.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

db_host = os.getenv("MYSQL_HOST")
db_name = os.getenv("MYSQL_DATABASE")  # Assuming this is the name of your database
try:
    # Connect to MySQL database
    db = mysql.connector.connect(
        host=db_host,
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=db_name,  # Specify the database
        port=os.getenv("MYSQL_PORT", 3306)
    )
    logging.info("Successfully connected to MySQL at %s:%s", db_host, os.getenv("MYSQL_PORT", 3306))

    cursor = db.cursor()

    # Create contacts table if it doesn't exist
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS contacts (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL
    )
    """)
    logging.info("Checked if contacts table exists (and created it if not).")

    # Insert dummy data
    dummy_data = [
        ('John Doe', 'john@example.com'),
        ('Jane Smith', 'jane@example.com'),
        ('Alice Johnson', 'alice@example.com')
    ]

    cursor.executemany("INSERT INTO contacts (name, email) VALUES (%s, %s)", dummy_data)
    db.commit()
    logging.info("Inserted dummy data into contacts table.")

except mysql.connector.Error as err:
    logging.error("Error: %s", err)
finally:
    if db.is_connected():
        cursor.close()
        db.close()
        logging.info("MySQL connection closed.")

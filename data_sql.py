import os
import mysql.connector
import logging
from flask import Flask, render_template, request, redirect
from db_functions import (get_contacts, findByNumber,
                          check_contact_exist, search_contacts,
                          create_contact, delete_contact, update_contact_in_db)

app = Flask(__name__)

# Configure logging
logging.basicConfig(filename='/tmp/app.log', level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Print environment variables for debugging
logging.debug("MYSQL_HOST: %s", os.getenv("MYSQL_HOST"))
logging.debug("MYSQL_USER: %s", os.getenv("MYSQL_USER"))
logging.debug("MYSQL_PASSWORD: %s", os.getenv("MYSQL_PASSWORD"))
logging.debug("MYSQL_DATABASE: %s", os.getenv("MYSQL_DATABASE"))
logging.debug("MYSQL_PORT: %s", os.getenv("MYSQL_PORT", 3306))

# Ensure MySQL connection uses the right host
db_host = os.getenv("MYSQL_HOST")
if not db_host or db_host == 'localhost':
    logging.error("MySQL host is not set correctly!")
    raise Exception("MySQL host is not set correctly!")

# Function to create the database and table
def create_database_and_table(cursor):
    try:
        # Create database if it doesn't exist
        cursor.execute("CREATE DATABASE IF NOT EXISTS contacts_app;")
        logging.info("Database 'contacts_app' created or already exists.")
        
        # Select the created database
        cursor.execute("USE contacts_app;")
        logging.info("Switched to database 'contacts_app'.")
        
        # Create contacts table if it doesn't exist
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS contacts (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL
        )
        """)
        logging.info("Table 'contacts' created or already exists.")
        
        # Insert dummy data into the contacts table
        cursor.execute("""
        INSERT INTO contacts (name, email)
        VALUES ('John Doe', 'john.doe@example.com'),
               ('Jane Smith', 'jane.smith@example.com')
        """)
        logging.info("Dummy data inserted into 'contacts' table.")
        
    except mysql.connector.Error as err:
        logging.error("Failed setting up the database or table: %s", err)
        raise

# Establish MySQL connection and create the database
def setup_database():
    try:
        db = mysql.connector.connect(
            host=db_host,
            user=os.getenv("MYSQL_USER"),
            password=os.getenv("MYSQL_PASSWORD"),
            port=os.getenv("MYSQL_PORT", 3306)
        )
        logging.info("Successfully connected to MySQL at %s:%s", db_host, os.getenv("MYSQL_PORT", 3306))
        cursor = db.cursor()
        create_database_and_table(cursor)
        db.commit()
        cursor.close()
        logging.info("Database setup completed successfully.")
        return True
    except mysql.connector.Error as err:
        logging.error("Error connecting to MySQL or setting up the database: %s", err)
        return False

# Run database setup and only start the Flask app if successful
if setup_database():
    logging.info("Starting Flask application...")
    app.run(debug=True, port=5052, host='0.0.0.0')
else:
    logging.error("Database setup failed. Flask application will not start.")

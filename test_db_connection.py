import os
import mysql.connector
import logging

# Configure logging
logging.basicConfig(filename='/tmp/db_test.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

db_host = os.getenv("MYSQL_HOST")

try:
    # Establish the connection
    db = mysql.connector.connect(
        host=db_host,
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        port=os.getenv("MYSQL_PORT", 3306),
        database="contacts_app"  # Ensure it connects to the correct database
    )
    logging.info("Successfully connected to MySQL at %s:%s", db_host, os.getenv("MYSQL_PORT", 3306))
    
    # Create cursor
    cursor = db.cursor()

    # Create contacts table if it doesn't exist
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS contacts (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL
    )
    """)
    logging.info("Table 'contacts' checked/created successfully.")

    # Insert dummy data
    cursor.execute("INSERT INTO contacts (name, email) VALUES ('John Doe', 'john@example.com')")
    cursor.execute("INSERT INTO contacts (name, email) VALUES ('Jane Smith', 'jane@example.com')")
    logging.info("Dummy data inserted into 'contacts' table.")

    # Commit the changes
    db.commit()
    logging.info("Changes committed successfully.")

except mysql.connector.Error as err:
    logging.error("Error connecting to MySQL: %s", err)

finally:
    # Close the cursor and connection
    if db.is_connected():
        cursor.close()
        db.close()
        logging.info("MySQL connection closed.")

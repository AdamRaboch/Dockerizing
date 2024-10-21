import mysql.connector
import logging

# Configure logging
logging.basicConfig(filename='mysql_connection.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Hardcoded values for testing
MYSQL_HOST = "mysql-service"
MYSQL_USER = "root"
MYSQL_PASSWORD = "admin"
MYSQL_DATABASE = "yourdatabase"
MYSQL_PORT = 3306

def connect_to_mysql():
    try:
        logging.info("Starting MySQL connection...")
        db = mysql.connector.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DATABASE,
            port=MYSQL_PORT
        )
        logging.info("Successfully connected to MySQL")
        cursor = db.cursor()
        cursor.execute("SHOW DATABASES")
        databases = cursor.fetchall()
        logging.info("Databases: %s", databases)
    except mysql.connector.Error as err:
        logging.error("Error: %s", err)
    finally:
        if db:
            db.close()
            logging.info("MySQL connection closed")

if __name__ == "__main__":
    connect_to_mysql()

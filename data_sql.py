# data_sql.py

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

# Establish MySQL connection
try:
    # Set up MySQL connection using environment variables
    db = mysql.connector.connect(
        host=db_host,
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DATABASE"),  # Added this to switch to the correct database
        port=os.getenv("MYSQL_PORT", 3306)
    )
    logging.info("Successfully connected to MySQL at %s:%s", db_host, os.getenv("MYSQL_PORT", 3306))

    # Create a cursor and call the function to create the database and table
    cursor = db.cursor()
    create_database_and_table(cursor)

    # Commit changes and close the cursor
    db.commit()
    cursor.close()
    logging.info("Database setup completed successfully.")

except mysql.connector.Error as err:
    logging.error("Error connecting to MySQL: %s", err)
    raise

# Flask app routes (merged from app.py)
@app.route('/')
def hello():
    logging.info("Redirecting to /viewContacts")
    return redirect('/viewContacts')

@app.route('/addContact', methods=['GET', 'POST'])
def addContact():
    if request.method == 'POST':
        logging.info("Received POST request to add contact")
    else:
        logging.info("Received GET request to display add contact form")
    return render_template('addContactForm.html')

@app.route('/viewContacts')
def viewContacts():
    logging.info("Fetching contacts")
    contacts = get_contacts()
    logging.info("Contacts fetched: %s", contacts)
    return render_template('index.html', contacts=contacts)

@app.route('/createContact', methods=['POST'])
def createContact():
    fullname = request.form['fullname']
    email = request.form['email']
    phone = request.form['phone']
    gender = request.form['gender']
    photo = request.files['photo']
    if not check_contact_exist(fullname, email):
        if photo:
            file_path = 'static/images/' + fullname + '.jpg'
            photo.save(file_path)
            logging.info("Photo saved for contact: %s", fullname)
        create_contact(fullname, phone, email, gender, f'{fullname}.jpg')
        logging.info("Contact created: %s", fullname)
    else:
        logging.warning("Contact already exists: %s", fullname)
        return render_template('addContactForm.html', message='Contact already exists')
    return redirect('/viewContacts')

@app.route('/deleteContact/<number>')
def deleteContact(number):
    delete_contact(number)
    logging.info("Contact deleted: %s", number)
    return redirect('/viewContacts')

@app.route('/editContact/<number>')
def editContact(number):
    contact = findByNumber(number)
    logging.info("Editing contact: %s", number)
    return render_template('editContactForm.html', contact=contact)

@app.route('/saveUpdatedContact/<number>', methods=['POST'])
def saveUpdatedContact(number):
    name = request.form['fullname']
    phone = request.form['phone']
    email = request.form['email']
    gender = request.form['gender']
    update_contact_in_db(number, name, phone, email, gender)
    logging.info("Contact updated: %s", number)
    return redirect('/viewContacts')

@app.route('/search', methods=['POST'])
def search():
    search_name = request.form['search_name']
    search_results = search_contacts(search_name)
    logging.info("Search performed for: %s, results count: %d", search_name, len(search_results))
    return render_template('index.html', contacts=search_results)

if __name__ == '__main__':
    app.run(debug=True, port=5052, host='0.0.0.0')

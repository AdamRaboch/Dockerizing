import os
import mysql.connector
import logging
from flask import Flask, render_template, request, redirect
from db_functions import (get_contacts, findByNumber,
                          check_contact_exist, search_contacts,
                          create_contact, delete_contact, update_contact)

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
        cursor.execute("CREATE DATABASE IF NOT EXISTS contacts_app;")
        logging.info("Database 'contacts_app' created or already exists.")
        
        cursor.execute("USE contacts_app;")
        logging.info("Switched to database 'contacts_app'.")
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS contacts (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            phone VARCHAR(255) NOT NULL,
            gender VARCHAR(50),
            photo VARCHAR(255)
        )
        """)
        logging.info("Table 'contacts' created or already exists.")
        
        cursor.execute("""
        INSERT INTO contacts (name, email, phone)
        VALUES ('John Doe', 'john.doe@example.com', '1234567890'),
               ('Jane Smith', 'jane.smith@example.com', '0987654321')
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
        db.close()
        logging.info("Database setup completed successfully.")
        return True
    except mysql.connector.Error as err:
        logging.error("Error connecting to MySQL or setting up the database: %s", err)
        return False

# Run database setup and only start the Flask app if successful
if setup_database():
    logging.info("Starting Flask application...")

    @app.route('/')
    def home():
        contacts = get_contacts()  # Retrieve contacts from the database
        return render_template('index.html', contacts=get_contacts())

    @app.route('/addContact', methods=['GET', 'POST'])
    def addContact():
        return render_template('addContactForm.html')
    
    @app.route('/createContact', methods=['GET', 'POST'])
    def createContact():
        if request.method == 'POST':
            fullname = request.form['fullname']
            email = request.form['email']
            phone = request.form['phone']  
            gender = request.form['gender']
            photo = request.files['photo']

            if not check_contact_exist(fullname, email):
                if photo:
                    # Create a name for the file to be saved
                    file_path = 'static/images/' + fullname + '.jpg'
                    # Save the file on the server  
                    photo.save(file_path)
                # Create a new contact
                create_contact(fullname, phone, email, gender, f'{fullname}.jpg')
                return redirect('/viewContacts')
            else:
                return render_template('addContactForm.html', error_message='Contact already exists')
        return render_template('addContactForm.html')

    @app.route('/viewContacts')
    def viewContacts():
        contacts = get_contacts()  # Retrieve contacts from the database
        return render_template('index.html', contacts=get_contacts())

    @app.route('/deleteContact/<int:id>')
    def delete_contact_route(id):
        def delete_contact(id);
        return redirect('/viewContacts')  # Redirect to the contacts page after deletion



    @app.route('/search', methods=['POST'])
    def search():
        search_name = request.form['search_name']
        search_results = search_contacts(search_name)
        return render_template('contacts_table.html', contacts=search_results)

    @app.route('/editContact/<int:number>')
    def editContact(number):
        contact = findByNumber(number)
        return render_template('editContactForm.html', contact=contact)

    @app.route('/saveUpdatedContact/<int:number>', methods=['POST'])
    def saveUpdatedContact(number):
        name = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        gender = request.form['gender']
        update_contact(number, name, phone, email, gender)
        return redirect('/viewContacts')

    # Start the Flask application
    app.run(debug=True, port=5052, host='0.0.0.0')
else:
    logging.error("Database setup failed. Flask application will not start.")

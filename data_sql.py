from flask import Flask, render_template, request, redirect
import os
import mysql.connector
import logging

from data_sql import (get_contacts, findByNumber,
                      check_contact_exist, search_contacts,
                      create_contact, delete_contact, update_contact_in_db)

app = Flask(__name__)

# Configure logging
logging.basicConfig(filename='/tmp/app.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Print environment variables for debugging
logging.info("MYSQL_HOST: %s", os.getenv("MYSQL_HOST"))
logging.info("MYSQL_USER: %s", os.getenv("MYSQL_USER"))
logging.info("MYSQL_PASSWORD: %s", os.getenv("MYSQL_PASSWORD"))
logging.info("MYSQL_DATABASE: %s", os.getenv("MYSQL_DATABASE"))
logging.info("MYSQL_PORT: %s", os.getenv("MYSQL_PORT", 3306))

# Ensure MySQL connection uses the right host
db_host = os.getenv("MYSQL_HOST")
if not db_host or db_host == 'localhost':
    logging.error("MySQL host is not set correctly!")
    raise Exception("MySQL host is not set correctly!")

try:
    # Set up MySQL connection using environment variables
    db = mysql.connector.connect(
        host=db_host,
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DATABASE"),
        port=os.getenv("MYSQL_PORT", 3306)
    )
    logging.info("Successfully connected to MySQL")
except mysql.connector.Error as err:
    logging.error("Error: %s", err)
    raise

@app.route('/')
def hello():
    return redirect('/viewContacts')

@app.route('/addContact', methods=['GET', 'POST'])
def addContact():
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
        create_contact(fullname, phone, email, gender, f'{fullname}.jpg')
    else:
        return render_template('addContactForm.html', message='Contact already exists')
    return redirect('/viewContacts')

@app.route('/deleteContact/<number>')
def deleteContact(number):
    delete_contact(number)
    return redirect('/viewContacts')

@app.route('/editContact/<number>')
def editContact(number):
    contact = findByNumber(number)
    return render_template('editContactForm.html', contact=contact)

@app.route('/saveUpdatedContact/<number>', methods=['POST'])
def saveUpdatedContact(number):
    name = request.form['fullname']
    phone = request.form['phone']
    email = request.form['email']
    gender = request.form['gender']
    update_contact_in_db(number, name, phone, email, gender)
    return redirect('/viewContacts')

@app.route('/search', methods=['POST'])
def search():
    search_name = request.form['search_name']
    search_results = search_contacts(search_name)
    return render_template('index.html', contacts=search_results)

if __name__ == '__main__':
    app.run(debug=True, port=5052, host='0.0.0.0')

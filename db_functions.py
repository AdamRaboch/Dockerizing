import mysql.connector
import os

# Function to establish a connection to the MySQL database
def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DATABASE"),
        port=os.getenv("MYSQL_PORT", 3306)
    )

def get_contacts():
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM contacts")
    result = cursor.fetchall()
    cursor.close()
    db.close()
    return result

def findByNumber(id):
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM contacts WHERE number = %s", (id,))
    result = cursor.fetchone()
    cursor.close()
    db.close()
    return result

def check_contact_exist(name, email):
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM contacts WHERE name = %s OR email = %s", (name, email))
    result = cursor.fetchone()
    cursor.close()
    db.close()
    return bool(result)

def search_contacts(search_name):
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM contacts WHERE name LIKE %s", ('%' + search_name + '%',))
    result = cursor.fetchall()
    cursor.close()
    db.close()
    return result

def create_contact(name, phone, email, gender, photo):
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("INSERT INTO contacts (name, phone, email, gender, photo) VALUES (%s, %s, %s, %s, %s)",
                   (name, phone, email, gender, photo))
    db.commit()
    cursor.close()
    db.close()
    return "Contact added successfully"

def delete_contact(id):
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("DELETE FROM contacts WHERE id = %s", (id,))
    db.commit()
    cursor.close()
    db.close()
    return "Contact deleted successfully"

def update_contact(number, name, phone, email, gender):
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("UPDATE contacts SET name = %s, phone = %s, email = %s, gender = %s WHERE number = %s",
                   (name, phone, email, gender, number))
    db.commit()
    cursor.close()
    db.close()

import psycopg2
import os
from passlib.hash import pbkdf2_sha256 as sha256

class DatabaseConnection:
    def __init__(self):
        db = 'd8l5eq5eakmkcm'
        # db = 'sendit'
        if os.getenv('APP_SETTINGS') == 'testing':
            db = 'test_db'
        # conn = psycopg2.connect(host="localhost", database=db, user="postgres", password="psql")
        conn = psycopg2.connect(host="ec2-23-23-101-25.compute-1.amazonaws.com", database=db, user="etpyvilhgiqvvw", password="999f624546819f9983ca1f6885672a281c4fe8ea23cbe3af4e42b98254b57cdd", port=5432)
        conn.autocommit = True
        self.cursor = conn.cursor()
        print (self.cursor)
        print(db)

    def generate_hash(password):
        return sha256.hash(password)

    def setUp(self):
        users_table = """CREATE TABLE IF NOT EXISTS users(
            user_id SERIAL PRIMARY KEY,
            user_name VARCHAR(25) UNIQUE NOT NULL,
            password VARCHAR(225) NOT NULL,
            admin BOOLEAN DEFAULT False
        )"""
        self.cursor.execute(users_table)

        parcels_table = """CREATE TABLE IF NOT EXISTS parcels(
            parcel_id SERIAL PRIMARY KEY,
            user_id VARCHAR(25) REFERENCES users (user_name),
            recipient_name VARCHAR(25) NOT NULL,
            recipient_mobile VARCHAR(25) NOT NULL,    
            pickup_location VARCHAR(25) NOT NULL,
            destination VARCHAR(25) NOT NULL,
            weight INTEGER NOT NULL,
            total_price INTEGER NOT NULL,
            status VARCHAR(25) DEFAULT 'pending',
            present_location VARCHAR(25) DEFAULT 'office'
        )"""
        self.cursor.execute(parcels_table)

        password = DatabaseConnection.generate_hash("root")
        
        check_no_of_rows = "SELECT * FROM users"
        self.cursor.execute(check_no_of_rows)
        result = self.cursor.fetchall()
        if len(result)==0:
            insert_admin = "INSERT INTO users (user_name, password) values ('admin', '{}')".format(password)
            update_to_admin = "UPDATE users set admin = True where user_name = 'admin'"
            self.cursor.execute(insert_admin)
            self.cursor.execute(update_to_admin)

        
    def insert_user(self, user_name, password):
        insert_user = "INSERT INTO users (user_name, password) values ('{}', '{}')".format(user_name, password)
        self.cursor.execute(insert_user)

    def login_user(self, user_name, password):
        select_user = "SELECT user_name, password FROM users WHERE user_name = '{}' and password = '{}'".format(user_name, password)
        self.cursor.execute(select_user)
        return [user_name,password]

    def add_parcel(self, user_id, recipient_name, recipient_mobile, pickup_location, destination, weight, total_price):
        insert_parcel = "INSERT INTO parcels (user_id, recipient_name, recipient_mobile, pickup_location, destination,  weight, total_price) values ('{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(user_id, recipient_name, recipient_mobile, pickup_location, destination, weight, total_price)
        self.cursor.execute(insert_parcel)

    def get_all_parcels(self):
        get_parcels = "SELECT * FROM parcels"
        self.cursor.execute(get_parcels)
        result = self.cursor.fetchall()
        return result

    def get_a_parcel(self, parcel_id):
        get_parcel = "SELECT * FROM parcels WHERE parcel_id = '{}'".format(parcel_id)
        self.cursor.execute(get_parcel)
        result = self.cursor.fetchone()
        return result

    def get_parcels_by_user(self, user_id):
        get_user_parcels = "SELECT * FROM parcels WHERE user_id = '{}'".format(user_id)
        self.cursor.execute(get_user_parcels)
        result = self.cursor.fetchone()
        return result

    def change_location(self, parcel_id, present_location):
        location = "UPDATE parcels SET present_location = '{}' WHERE parcel_id = '{}'".format(present_location, parcel_id)
        self.cursor.execute(location)
        return present_location

    def change_destination(self, parcel_id, destination):
        destination = "UPDATE parcels SET destination = '{}' WHERE parcel_id = '{}'".format(destination, parcel_id)
        self.cursor.execute(destination)
        return destination

    def change_status(self, parcel_id, status):
        status = "UPDATE parcels SET status = '{}' WHERE parcel_id = '{}'".format(status, parcel_id)
        self.cursor.execute(status)

    def get_user(self, user_name):
        get_user_parcels = "SELECT * FROM users WHERE user_name = '{}'".format(user_name)
        self.cursor.execute(get_user_parcels)
        result = self.cursor.fetchone()
        return result

    def get_users(self):
        get_users = "SELECT * FROM users"
        self.cursor.execute(get_users)
        result = self.cursor.fetchall()
        return result

    def delete_tables(self):
        delete = "DROP TABLE users, parcels"
        self.cursor.execute(delete)

    
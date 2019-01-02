import psycopg2
import os
from passlib.hash import pbkdf2_sha256 as sha256

class DatabaseConnection:
    def __init__(self):

        db = 'd8l5eq5eakmkcm'
#         db = 'sendit'
        if os.getenv('APP_SETTINGS') == 'testing':
            db = 'test_db'
#         conn = psycopg2.connect(host="localhost", database=db, user="postgres", password="psql")
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
            user_email VARCHAR(25) UNIQUE NOT NULL,
            user_mobile VARCHAR(25) NOT NULL,
            user_password VARCHAR(225) NOT NULL,
            admin_status BOOLEAN DEFAULT False,
            default_pickup_location VARCHAR(225) NULL,
            img bytea
        )"""
        self.cursor.execute(users_table)


        parcels_table = """CREATE TABLE IF NOT EXISTS parcels(
            parcel_id SERIAL PRIMARY KEY,
            description VARCHAR NOT NULL,
            user_id INTEGER NOT NULL,
            user_name VARCHAR(25) NOT NULL,
            recipient_name VARCHAR(25) NOT NULL,
            recipient_mobile VARCHAR(25) NOT NULL,    
            pickup_location VARCHAR(225) NOT NULL,
            destination VARCHAR(225) NOT NULL,
            weight INTEGER NOT NULL,
            total_price INTEGER NOT NULL,
            status VARCHAR(25) DEFAULT 'pending',
            present_location VARCHAR(25) NOT NULL,
            date_created DATE NOT NULL DEFAULT CURRENT_DATE
        )"""
        self.cursor.execute(parcels_table)

        password = DatabaseConnection.generate_hash("rootsroot")
        check_no_of_rows = "SELECT * FROM users"
        self.cursor.execute(check_no_of_rows)
        result = self.cursor.fetchall()
        if len(result)==0:
            insert_admin = "INSERT INTO users (user_name, user_email, user_mobile, user_password) values ('admin', 'admin@gmail.com', '0780456734', '{}')".format(password)
            update_to_admin = "UPDATE users set admin_status = True where user_name = 'admin'"
            # insert_img = "UPDATE users SET img = bytea('/home/daizy/Andela/Bootcamp14/Send_IT_APIs/app/controllers/dee.jpg') where user_name = 'admin'"
            self.cursor.execute(insert_admin)
            self.cursor.execute(update_to_admin)
            # self.cursor.execute(insert_img)
          
    def insert_user(self, user_name, user_email, user_mobile, user_password):
        insert_user = "INSERT INTO users (user_name, user_email, user_mobile, user_password) values ('{}', '{}', '{}', '{}')".format(user_name, user_email, user_mobile, user_password)
        self.cursor.execute(insert_user)

    def clear_data(self, user_name):
        delete_content = "UPDATE users SET user_email = '' WHERE user_name = '{}'".format(user_name)
        self.cursor.execute(delete_content)
        return user_name

    def edit_user(self, user_email, user_mobile, default_pickup_location, user_name,):
        update = " UPDATE users SET (user_email, user_mobile, default_pickup_location) = ('{}', '{}', '{}') WHERE user_name = '{}' ".format(user_email, user_mobile, default_pickup_location, user_name)
        self.cursor.execute(update)
        print(update)

    def login_user(self, user_name, user_password):
        select_user = "SELECT user_name, user_password FROM users WHERE user_name = '{}' and user_password = '{}'".format(user_name, user_password)
        self.cursor.execute(select_user)
        return [user_name,user_password]

    def add_parcel(self, description, user_id, user_name, recipient_name, recipient_mobile, pickup_location, destination, weight, total_price):
        insert_parcel = "INSERT INTO parcels (description, user_id, user_name, recipient_name, recipient_mobile, pickup_location, destination,  weight, total_price, present_location) values ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(description, user_id, user_name, recipient_name, recipient_mobile, pickup_location, destination, weight, total_price, pickup_location)
        self.cursor.execute(insert_parcel)

    def get_all_parcels(self):
        get_parcels = "SELECT * FROM parcels ORDER BY parcel_id ASC"
        self.cursor.execute(get_parcels)
        result = self.cursor.fetchall()
        return result

    def get_a_parcel(self, parcel_id):
        get_parcel = "SELECT * FROM parcels WHERE parcel_id = '{}'".format(parcel_id)
        self.cursor.execute(get_parcel)
        result = self.cursor.fetchone()
        return result

    def get_user_parcels_by_status(self, user_id, status):
        get_user_parcels = "SELECT * FROM parcels WHERE user_id = '{}' and status = '{}' ORDER BY parcel_id ASC".format(user_id, status)
        self.cursor.execute(get_user_parcels)
        result = self.cursor.fetchall()
        return result

    def get_parcels_by_user(self, user_id):
        get_user_parcels = "SELECT * FROM parcels WHERE user_id = '{}' ORDER BY parcel_id ASC".format(user_id)
        self.cursor.execute(get_user_parcels)
        result = self.cursor.fetchall()
        return result

    def change_location(self, parcel_id, present_location):
        location = "UPDATE parcels SET present_location = '{}' WHERE parcel_id = '{}'".format(present_location, parcel_id)
        self.cursor.execute(location)
        return present_location

    def change_destination(self, parcel_id, destination, price):
        destination = "UPDATE parcels SET destination = '{}', total_price = '{}' WHERE parcel_id = '{}'".format(destination, price, parcel_id)
        self.cursor.execute(destination)
        return destination

    def change_status(self, parcel_id, status):
        status = "UPDATE parcels SET status = '{}' WHERE parcel_id = '{}'".format(status, parcel_id)
        self.cursor.execute(status)

    def get_user(self, user_name):
        get_user = "SELECT * FROM users WHERE user_name = '{}'".format(user_name)
        self.cursor.execute(get_user)
        result = self.cursor.fetchone()
        return result

    def get_user_by_id(self, user_id):
        get_user = "SELECT * FROM users WHERE user_id = '{}'".format(user_id)
        self.cursor.execute(get_user)
        result = self.cursor.fetchone()
        return result

    def get_users(self):
        get_users = "SELECT * FROM users ORDER BY user_id ASC"
        self.cursor.execute(get_users)
        result = self.cursor.fetchall()
        return result

    def change_user_role_to_admin(self, user_id):
        update_role_to_admin = "UPDATE users set admin_status = True where user_id = '{}'".format(user_id)
        self.cursor.execute(update_role_to_admin)

    def change_user_role_to_user(self, user_id):
        update_role_to_regular_user = "UPDATE users set admin_status = False where user_id = '{}'".format(user_id)
        self.cursor.execute(update_role_to_regular_user)

    def delete_tables(self):
        delete = "DROP TABLE users, parcels"
        self.cursor.execute(delete)

    
    def select_no_of_user_parcels(self, username):
        query = "SELECT COUNT(user_name) FROM parcels WHERE user_name = '{}'".format(username)
        self.cursor.execute(query)
        result = self.cursor.fetchone()
        return result

    def select_no_of_user_parcels_cancelled(self, username):
        query = "SELECT COUNT(user_name) FROM parcels WHERE user_name = '{}' and status = 'cancelled'".format(username)
        self.cursor.execute(query)
        result = self.cursor.fetchone()
        return result

    def select_no_of_user_parcels_pending(self, username):
        query = "SELECT COUNT(user_name) FROM parcels WHERE user_name = '{}' and status = 'pending'".format(username)
        self.cursor.execute(query)
        result = self.cursor.fetchone()
        return result

    def select_no_of_user_parcels_intransit(self, username):
        query = "SELECT COUNT(user_name) FROM parcels WHERE user_name = '{}' and status = 'intransit'".format(username)
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        return result

    def select_no_of_user_parcels_delivered(self, username):
        query = "SELECT COUNT(user_name) FROM parcels WHERE user_name = '{}' and status = 'delivered'".format(username)
        self.cursor.execute(query)
        result = self.cursor.fetchone()
        return result

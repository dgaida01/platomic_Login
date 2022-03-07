from flask_app.config.mysqlconnection import connectToMySQL
import re
from flask import flash
from flask_app import app
from flask_bcrypt import Bcrypt
# MySQL connector: pipenv install pymysql
# password encryption: pipenv install flask-bcrypt
bcrypt = Bcrypt(app)

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
INVALIDS = re.compile(r'[^0-9a-zA-Z!@#$%^&*()?._-]')


class User:

    def __init__(self, data):
        self.id = data['id']
        self.email = data['email']
        self.password = data['password']
        self.verified = data['verified']
        self.secret = data['secret']
        self.use_two_factor = data['use_two_factor']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    # def __repr__(self) -> str:
    #     return f"email:{self.email} verified:{self.verified} use_two_factor:{self.use_two_factor}"

    @classmethod
    def insert_new_user(cls, data):
        query = '''INSERT INTO users (password,verified) VALUES (%(password)s,True);'''
        data['user_id'] = connectToMySQL().query_db(query, data)
        query = '''INSERT INTO emails(email, user_id, is_primary) 
                VALUES (%(email)s, %(user_id)s, True);'''
        connectToMySQL().query_db(query, data)
        return data['user_id']

# =======================
    # GET UNIQUE USER
# =======================

    @classmethod
    def get_user_by_id(cls, data):
        query = 'SELECT users.*, emails.email FROM users LEFT JOIN emails  ON emails.user_id = users.id WHERE users.id = (%(id)s)'
        results = connectToMySQL().query_db(query, data)
       
        if len(results) < 1:
            return None
        print("++++++++++++++++++", results[0])
        result = cls(results[0])
        print("__________________", result)
        return result

    @classmethod
    def get_user_by_email(cls, data):
        query = '''SELECT users.*, emails.email FROM users LEFT JOIN emails 
                ON emails.user_id = users.id WHERE email =%(email)s'''
        results = connectToMySQL().query_db(query, data)
        if len(results) == 0:
            return None
        return cls(results[0])

    @classmethod
    def update_secret(cls,data):
        query = 'UPDATE users SET secret=%(secret)s, use_two_Factor=1 where id = %(id)s;'
        results = connectToMySQL().query_db(query,data)
        
        if results==None:
            return None
        return cls(results[0])


# =======================
    #  VALIDATION
# =======================

    @staticmethod
    def is_valid_email(email, login=False):
        if not EMAIL_REGEX.match(email):
            if not login:
                flash("Invalid email address.", "email")
            return False
        return True

    @staticmethod
    def is_existing_email(email, login=False):
        data = {
            'email': email
        }
        if User.get_user_by_email(data) == None:
            return False
        if not login:
            flash("Email already exists.", "email")
        return True

    @staticmethod
    def is_valid_password(password, login=False):
        is_valid = True
        if len(password) < 8 or len(password) > 32:
            if not login:
                flash("Passwords should be 8-32 characters", "password")
            is_valid = False

        if re.search("[a-z]", password) == None:
            if not login:
                flash("Password should contain a lowercase letter", "password")
            is_valid = False

        if re.search("[A-Z]", password) == None:
            if not login:
                flash("Password should contain at an uppercase letter", "password")
            is_valid = False

        if re.search("[0-9]", password) == None:
            if not login:
                flash("Password should contain a number", "password")
            is_valid = False

        if re.search("[!@#$%^&*()?._-]", password) == None:
            if not login:
                flash(
                    "Password should contain a special character ex: !@#$%^&*()?._-", "password")
            is_valid = False

        if INVALIDS.match(password):
            if not login:
                flash(
                    "Password should only be alphanumeric or !@#$%^&*()?._- characters", "password")
            is_valid = False
        return is_valid

    @staticmethod
    def is_matching_password(confirm, password):
        if password != confirm:
            flash("Passwords do not match.", "confirm")
            return False
        return True

    @staticmethod
    def is_valid_new_user(user):
        is_valid = True

        if not User.is_valid_email(user['email']):
            is_valid = False
        if User.is_existing_email(user['email']):
            is_valid = False
        if not User.is_valid_password(user['password']):
            is_valid = False
        if not User.is_matching_password(user['confirm_password'], user['password']):
            is_valid = False

        return is_valid

    @staticmethod
    def login(data):
        user = None        
        if not User.is_valid_email(data['email'], login=True):
            flash("Invalid Login/Password", "login")
            return False
        user = User.get_user_by_email(data)
        if user == None:
            flash("Invalid Login/Password", "login")
            return False
        return user

from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, redirect, request
from flask_app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__(self, data):
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.password = data["password"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    @staticmethod
    def validate_register(data):
        is_valid = True
        if len(data["first_name"]) < 3:
            flash("First name must contain at least 5 characters.")
            is_valid = False
        if len(data["last_name"]) < 3:
            flash("First name must contain at least 5 characters.")
            is_valid = False
        if not EMAIL_REGEX.match(data["email"]):
            flash("Enter a valid email.")
            is_valid = False
        if User.get_by_email(data):
            flash("Email already in use. Login or register different email.")
        if len(data["password"]) < 8:
            flash("Password must contain at least 8 characters.")
            is_valid = False
        if data["password"] != data["pass_conf"]:
            flash("Passwords do not match.")
            is_valid = False
        return is_valid

    @staticmethod
    def validate_login(data):
        is_valid = True

        user_in_db = User.get_by_email(data)
        if not user_in_db:
            flash("Invalid Email or Password")
            is_valid = False
        elif not bcrypt.check_password_hash(user_in_db.password, data["password"]):
            flash("Invalid Email or Password")
            is_valid = False
        return is_valid

    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL("artists_paintings").query_db(query, data)
        # Didn't find a matching user
        if len(result) < 1:
            return False
        return cls(result[0])

    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(user_id)s;"
        result = connectToMySQL("artists_paintings").query_db(query, data)
        # Didn't find a matching user
        if len(result) < 1:
            return False
        return cls(result[0])

    @classmethod
    def create_user(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password, created_at) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW());"
        results = connectToMySQL("artists_paintings").query_db(query, data)
        return results

        
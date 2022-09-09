import re
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user

class Painting:
    def __init__(self, data):
        self.id = data["id"]
        self.title = data["title"]
        self.description = data["description"]
        self.price = data["price"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.user_id = data["user_id"]

        self.user = {}

    @staticmethod
    def validate_painting(data):
        is_valid = True
        if len(data['title']) < 2:
            flash("Title must be 2 characters or more.")
            is_valid = False
        if len(data["description"]) < 1:
            flash('Description must be 10 or more characters.')
            is_valid = False
        if len(data["price"]) <= 0:
            flash('Price must be greater than 0.')
            is_valid = False
        return is_valid
    @classmethod
    def create_painting(cls, data):
        query = "INSERT INTO paintings (title, description, price, user_id, created_at) VALUES (%(title)s, %(description)s, %(price)s, %(user_id)s, NOW());"
        results = connectToMySQL("artists_paintings").query_db(query, data)
        return results

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM paintings LEFT JOIN users ON paintings.user_id = users.id;"
        results = connectToMySQL("artists_paintings").query_db(query)

        all_paintings = []

        for row in results:
            painting = cls(row)

            user_data = {
                "id" : row["users.id"],
                "first_name" : row["first_name"],
                "last_name" : row["last_name"],
                "email" : row["email"],
                "password" : row["password"],
                "created_at" : row["users.created_at"],
                "updated_at" : row["users.updated_at"]
            }
            painting.user = user.User(user_data)
            all_paintings.append(painting)
        return all_paintings

    @classmethod
    def get_painting_with_user(cls, data):
        query = "SELECT * FROM paintings LEFT JOIN users ON paintings.user_id = users.id WHERE paintings.id = %(painting_id)s;"
        results = connectToMySQL("artists_paintings").query_db(query, data)

        painting = cls(results[0])
        user_data = {
            "id" : results[0]["users.id"],
            "first_name" : results[0]["first_name"],
            "last_name" : results[0]["last_name"],
            "email" : results[0]["email"],
            "password" : results[0]["password"],
            "created_at" : results[0]["users.created_at"],
            "updated_at" : results[0]["users.updated_at"]
        }

        painting.user = user.User(user_data)
        return painting

    @classmethod
    def update_painting_info(cls, data):
        query = "UPDATE paintings SET title = %(title)s, description = %(description)s, price = %(price)s, updated_at = NOW() WHERE id = %(painting_id)s;"
        results = connectToMySQL("artists_paintings").query_db(query, data)
        return


    @classmethod
    def delete_painting(cls, data):
        query = "DELETE FROM paintings WHERE id = %(painting_id)s;"
        results = connectToMySQL("artists_paintings").query_db(query, data)
        return
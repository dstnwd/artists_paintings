from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.painting import Painting

@app.route("/new_painting")
def new_painting():
    if "user_id" not in session:
        flash("Please login or register")
        return redirect("/")

    return render_template("new_painting.html")

@app.route("/create_painting", methods=["POST"])
def create_painting():
    data = {
        "title" : request.form["title"],
        "description" : request.form["description"],
        "price" : request.form["price"],
        "user_id" : session["user_id"]
    }
    print(data)
    if not Painting.validate_painting(data):
        return redirect("/new_painting")

    Painting.create_painting(data)

    return redirect("/dashboard")

@app.route("/painting/<int:painting_id>")
def show_painting(painting_id):
    if "user_id" not in session:
        flash("Please login or register")
        return redirect("/")

    data = {
        "painting_id" : painting_id
    }

    painting = Painting.get_painting_with_user(data)

    return render_template("show_painting.html", painting = painting)

@app.route("/painting/<int:painting_id>/edit")
def edit_painting(painting_id):
    data = {
        "painting_id" : painting_id
    }

    painting = Painting.get_painting_with_user(data)

    return render_template("edit_painting.html", painting = painting)

@app.route("/painting/<int:painting_id>/update", methods=["POST"])
def update_painting(painting_id):
    data = {
        "title" : request.form["title"],
        "description" : request.form["description"],
        "price" : request.form["price"],
        "painting_id" : painting_id
    }

    if not Painting.validate_painting(data):
        return redirect(f"/painting/{painting_id}/edit")

    Painting.update_painting_info(data)

    return redirect("/dashboard")

@app.route("/painting/<int:painting_id>/delete")
def delete_painting(painting_id):
    data = {
        "painting_id" : painting_id
    }
    Painting.delete_painting(data)

    return redirect("/dashboard")


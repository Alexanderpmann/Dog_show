from flask_app import app
from flask import render_template, redirect, request, session, flash

from flask_app.models.dog import Dog
from flask_app.models.owner import Owner

# =================================================
# Create Dog Routes
# =================================================

@app.route("/new_dog")
def new_dog():
    if "owner_id" not in session:
        flash("Please login or register before entering the site!")
        return redirect("/")

    return render_template("new_dog.html", owner_id = session["owner_id"])

@app.route("/create_dog", methods=["POST"])
def create_dog():
    # 1 - validate form data
    # if no hidden input on form w/owner_id -> "owner_id" : session["owner_id"] instead
    data = {
        "name" : request.form["name"],
        "breed" : request.form["breed"],
        "age" : request.form["age"],
        "owner_id" : request.form["owner_id"]
    }

    if not Dog.validate_dog(data):
        return redirect("/new_dog")
    # 2 - save new dog to database
    Dog.create_dog(data)

    # 3 - redirect back to the dashboard page
    return redirect("/dashboard")

# =================================================
# Show One Dog Route
# =================================================

@app.route("/dog/<int:dog_id>")
def show_dog(dog_id):
    if "owner_id" not in session:
        flash("Please login or register before entering the site!")
        return redirect("/")

    # 1 - query for dog info w/associated info of owner
    data = {
        "dog_id" : dog_id
    }
    dog = Dog.get_dog_with_owner(data)

    # 2 - send info to show page

    return render_template("show_dog.html", dog = dog)

# =================================================
# Edit One Dog Route
# =================================================

@app.route("/dog/<int:dog_id>/edit")
def edit_dog(dog_id):
    # 1 - query for the dog we want to update
    data = {
        "dog_id" : dog_id
    }
    dog = Dog.get_dog_with_owner(data)
    # 2 - pass dog info to the html
    return render_template("edit_dog.html", dog = dog)

@app.route("/dog/<int:dog_id>/update", methods=["POST"])
def update_dog(dog_id):
    # 1 - validate our form data
    data = {
        "name" : request.form["name"],
        "breed" : request.form["breed"],
        "age" : request.form["age"],
        "dog_id" : dog_id
    }

    if not Dog.validate_dog(data):
        return redirect(f"/dog/{dog_id}/edit")
    # 2 - update information    
    Dog.update_dog_info(data)
    # 3 - redirect to dashboard

    return redirect("/dashboard")

# =================================================
# Delete One Dog Route
# =================================================

@app.route("/dog/<int:dog_id>/delete")
def delete_dog(dog_id):
    # 1 - delete dog
    data = {
        "dog_id" : dog_id
    }
    Dog.delete_dog(data)

    # 2 - redirect to dashboard
    return redirect("/dashboard")
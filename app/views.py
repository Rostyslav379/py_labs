import json
import uuid

from flask import Flask, request

app = Flask(__name__)

USERS_DATA_FILE = "app/users.json"
CATEGORIES_DATA_FILE = "app/categories.json"


def load_data(data_filepath):
    try:
        with open(data_filepath, "r") as file:
            return json.load(file)
    except FileNotFoundError as e:
        return {}

def save_data(data, data_filepath):
    with open(data_filepath, "w") as file:
        json.dump(data, file, indent=4)

users = load_data(USERS_DATA_FILE)
categories = load_data(CATEGORIES_DATA_FILE)
@app.route("/healthcheck")
def healthcheck():
    return "<p>healthcheck</p>"

# // user

@app.post("/user")
def create_user():
    user_data = request.get_json()
    user_id = uuid.uuid4().hex
    user = {"id": user_id, **user_data}
    users.append(user)
    save_data(users,USERS_DATA_FILE)
    return user

@app.get("/users")
def get_users():
    return list(users)

@app.get("/user/<user_id>")
def get_user_by_id(user_id: str):
     for element in list(users):
         if element["id"] == user_id:
            return element


@app.delete("/user/<user_id>")
def delete_user_by_id(user_id: str):
     for element in list(users):
         if element["id"] == user_id:
            users.remove(element)
            save_data(users,USERS_DATA_FILE)
            return json.encoder.encode_basestring(element["id"])



# // category

@app.post("/category")
def create_category():
    category_data = request.get_json()
    category_id = uuid.uuid4().hex
    category = {"id": category_id, **category_data}
    categories.append(category)
    save_data(categories, CATEGORIES_DATA_FILE)
    return category
@app.get("/category")
def get_category():
    return list(categories)

@app.delete("/category/<category_id>")
def delete_category_by_id(category_id: str):
     for element in list(categories):
         if element["id"] == category_id:
            categories.remove(element)
            save_data(categories,CATEGORIES_DATA_FILE)
            return json.encoder.encode_basestring(element["id"])
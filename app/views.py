from flask import Flask
import json

app = Flask(__name__)

def load_data(data_filepath):
    try:
        with open(data_filepath, "r") as file:
            return json.load(file)
    except FileNotFoundError as e:
        return {}

def save_data(data, data_filepath):
    with open(data_filepath, "w") as file:
        json.dump(data, file, indent=4)

@app.route("/healthcheck")
def healthcheck():
    return "<p>healthcheck</p>"

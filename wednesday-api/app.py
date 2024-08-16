import csv
import random

from flask import Flask, jsonify, make_response

app = Flask(__name__)


@app.route("/")
def root():
    wednesday_list = []
    with open("wednesday.csv", newline="") as csvfile:
        reader = csv.DictReader(
            csvfile, delimiter=";", fieldnames=["quote", "attribution"]
        )
        for row in reader:
            wednesday_list.append(dict(row))
    random_quote = random.choice(wednesday_list)
    return jsonify(quote=random_quote["quote"], attribution=random_quote["attribution"])


@app.errorhandler(404)
def resource_not_found(e):
    return make_response(jsonify(error="Not found!"), 404)


if __name__ == "__main__":
    root()

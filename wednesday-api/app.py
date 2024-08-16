import csv
import random
from datetime import datetime

from flask import Flask, jsonify, make_response, request

app = Flask(__name__)


@app.route("/")
def root():
    fake_wednesday = request.args.get('it_is_wednesday_in_my_heart')
    if not fake_wednesday:
        today = datetime.now()
        if today.weekday() != 2:
            return jsonify(message="It is not Wednesday"), 425

    # Read in the CSV to a list of dicts
    wednesday_list = []
    with open("wednesday.csv", newline="") as csvfile:
        reader = csv.DictReader(
            csvfile, delimiter=";", fieldnames=["quote", "attribution"]
        )
        for row in reader:
            wednesday_list.append(dict(row))

    # Select a random quote
    random_quote = random.choice(wednesday_list)

    # Return the random quote
    return jsonify(quote=random_quote["quote"], attribution=random_quote["attribution"])


@app.errorhandler(404)
def resource_not_found(e):
    return make_response(jsonify(error="Not found!"), 404)


if __name__ == "__main__":
    root()

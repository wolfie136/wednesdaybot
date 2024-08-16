import csv
import random
import os
from datetime import datetime
from mastodon import Mastodon
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

    mastodon = Mastodon(
        access_token = os.environ.get("MASTODON_ACCESS_TOKEN", ""),
        api_base_url = os.environ.get("MASTODON_BASE_URL", "")
    )

    # Toot
    toot_text = random_quote["quote"]
    if "attribution" in random_quote:
        toot_text = toot_text + " - " + random_quote["attribution"]

    mastodon.status_post(toot_text)

    # Return the random quote
    return jsonify(quote=random_quote["quote"], attribution=random_quote["attribution"])


@app.errorhandler(404)
def resource_not_found(e):
    return make_response(jsonify(error="Not found!"), 404)


if __name__ == "__main__":
    root()

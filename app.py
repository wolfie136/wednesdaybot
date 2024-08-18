import csv
import os
import random
from datetime import datetime
import logging

from flask import Flask, jsonify, make_response, request
from mastodon import Mastodon

app = Flask(__name__)

if logging.getLogger().hasHandlers():
    # The Lambda environment pre-configures a handler logging to stderr. If a handler is already configured,
    # `.basicConfig` does not execute. Thus we set the level directly.
    logging.getLogger().setLevel(logging.INFO)
else:
    logging.basicConfig(level=logging.INFO)


def toot_quote(quote_dict):
    mastodon = Mastodon(
        access_token=os.environ.get("MASTODON_ACCESS_TOKEN", ""),
        api_base_url=os.environ.get("MASTODON_BASE_URL", ""),
    )

    # Toot
    toot_text = quote_dict["quote"]
    if "attribution" in quote_dict and quote_dict["attribution"]:
        toot_text = toot_text + " - " + quote_dict["attribution"]

    logging.info(f"Tooting quote: {toot_text}")
    mastodon.status_post(toot_text)


def toot_random_quote(event=None, context=None):
    if is_it_wednesday():
        random_quote = random.choice(load_quotes())
        toot_quote(random_quote)
    else:
        logging.info("Not tooting because it is not Wednesday")


def load_quotes():
    # Read in the CSV to a list of dicts
    wednesday_list = []
    with open("wednesday.csv", newline="") as csvfile:
        reader = csv.DictReader(
            csvfile, delimiter=";", fieldnames=["quote", "attribution"]
        )
        for row in reader:
            wednesday_list.append(dict(row))
    return wednesday_list


def is_it_wednesday(fake_wednesday=False):
    pretend_its_wednesday = fake_wednesday
    if os.environ.get("FAKE_WEDNESDAY", ""):
        pretend_its_wednesday = True
    if not pretend_its_wednesday:
        today = datetime.now()
        if today.weekday() != 2:
            return False
    return True


@app.route("/")
def root():
    # Check if it's Wednesday
    fake_wednesday = request.args.get("it_is_wednesday_in_my_heart")
    if not is_it_wednesday(fake_wednesday=fake_wednesday):
        return jsonify(message="It is not Wednesday"), 425

    # Select a random quote
    random_quote = random.choice(load_quotes())

    # Return the random quote
    return jsonify(quote=random_quote["quote"], attribution=random_quote["attribution"])


@app.errorhandler(404)
def resource_not_found(e):
    return make_response(jsonify(error="Not found!"), 404)


if __name__ == "__main__":
    toot_random_quote()

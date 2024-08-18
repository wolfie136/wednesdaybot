import logging
import random

from flask import Flask, jsonify, make_response, request

from utils import utils

app = Flask(__name__)

if logging.getLogger().hasHandlers():
    # The Lambda environment pre-configures a handler logging to stderr. If a handler is already configured,
    # `.basicConfig` does not execute. Thus we set the level directly.
    logging.getLogger().setLevel(logging.INFO)
else:
    logging.basicConfig(level=logging.INFO)


@app.route("/")
def root():
    # Check if it's Wednesday
    fake_wednesday = request.args.get("it_is_wednesday_in_my_heart")
    if not utils.is_it_wednesday(fake_wednesday=fake_wednesday):
        return jsonify(message="It is not Wednesday"), 425

    # Select a random quote
    random_quote = random.choice(utils.load_quotes())

    # Return the random quote
    return jsonify(quote=random_quote["quote"], attribution=random_quote["attribution"])


@app.errorhandler(404)
def resource_not_found(e):
    return make_response(jsonify(error="Not found!"), 404)

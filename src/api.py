import logging
import random

from flask import Blueprint, Flask, jsonify, make_response

from utils import utils

app = Flask(__name__)
api = Blueprint("api_v1", __name__)

if logging.getLogger().hasHandlers():
    # The Lambda environment pre-configures a handler logging to stderr. If a handler is already configured,
    # `.basicConfig` does not execute. Thus we set the level directly.
    logging.getLogger().setLevel(logging.INFO)
else:
    logging.basicConfig(level=logging.INFO)


@api.route("/quote")
def quote():
    quotes = utils.load_quotes()
    return jsonify(quotes)


@api.route("/quote/random")
def quote_random():
    random_quote = random.choice(utils.load_quotes())
    return jsonify(random_quote)


@api.route("/quote/<int:index>")
def quote_index(index):
    quote = utils.load_quotes()[index]
    return jsonify(quote)


@app.errorhandler(404)
def resource_not_found(e):
    return make_response(jsonify(error="Not found!"), 404)


app.register_blueprint(api, url_prefix="/v1")

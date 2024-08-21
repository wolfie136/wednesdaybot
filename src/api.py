import logging
import random

from flasgger import Swagger
from flask import Blueprint, Flask, jsonify, make_response

from utils import utils

app = Flask(__name__)
app.config["SWAGGER"] = {"title": "Wednesday API", "version": "1.0.0"}
swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": "apispec",
            "route": "/v1/spec.json",
            "rule_filter": lambda rule: True,  # all in
            "model_filter": lambda tag: True,  # all in
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/",
}
swagger = Swagger(app, config=swagger_config)
api = Blueprint("api_v1", __name__)


if logging.getLogger().hasHandlers():
    # The Lambda environment pre-configures a handler logging to stderr. If a handler is already configured,
    # `.basicConfig` does not execute. Thus we set the level directly.
    logging.getLogger().setLevel(logging.INFO)
else:
    logging.basicConfig(level=logging.INFO)


@api.route("/quote")
def quote():
    """Returns the full list of available quotes.
    ---
    definitions:
      QuoteList:
        type: array
        items:
          $ref: '#/definitions/Quote'
      Quote:
        type: object
        properties:
          quote:
            type: string
          attribution:
            type: string
    responses:
      200:
        description: A list of Wednesday quotes
        schema:
          $ref: '#/definitions/QuoteList'
    """
    quotes = utils.load_quotes()
    return jsonify(quotes)


@api.route("/quote/random")
def quote_random():
    """Returns a random quote.
    ---
    definitions:
      Quote:
        type: object
        properties:
          quote:
            type: string
          attribution:
            type: string
    responses:
      200:
        description: A Wednesday quote
        schema:
          $ref: '#/definitions/Quote'
    """
    random_quote = random.choice(utils.load_quotes())
    return jsonify(random_quote)


@api.route("/quote/<int:index>")
def quote_index(index):
    """Returns a specific quote.
    ---
    parameters:
      - name: index
        in: path
        type: integer
        required: true
    definitions:
      Quote:
        type: object
        properties:
          quote:
            type: string
          attribution:
            type: string
    responses:
      200:
        description: A Wednesday quote
        schema:
          $ref: '#/definitions/Quote'
    """
    quote = utils.load_quotes()[index]
    return jsonify(quote)


@app.errorhandler(404)
def resource_not_found(e):
    return make_response(jsonify(error="Not found!"), 404)


app.register_blueprint(api, url_prefix="/v1")

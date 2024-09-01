import logging
import random

from flasgger import Swagger
from flask import Blueprint, Flask, jsonify, make_response, request

from utils import dynamodb

app = Flask(__name__)
app.config["SWAGGER"] = {
    "title": "Wednesday API",
    "version": "1.0.0",
    "description": "An API for Wednesdays",
    "termsOfService": "Please be nice!",
}
swagger_config = Swagger.DEFAULT_CONFIG
swagger_config["swagger_ui"] = False
swagger_config["specs"][0]["route"] = "/v1/spec.json"
swagger = Swagger(app, config=swagger_config)
api = Blueprint("api_v1", __name__)


logging.basicConfig(format="%(asctime)s %(message)s", level=logging.INFO, force=True)


@api.route("/quotes")
def quotes():
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
    start_id = request.args.get("start_id")
    quotes, last_evaluated_key = dynamodb.get_quotes(start_id=start_id)
    api_root = "https://devapi.wednesday.zone/v1"
    response = {
        "links": {
            "self": (
                f"{api_root}/quotes?start_id={start_id}"
                if start_id
                else f"{api_root}/quotes"
            )
        },
        "data": quotes,
    }

    if last_evaluated_key:
        response["links"][
            "next"
        ] = f"{api_root}/quotes?start_id={last_evaluated_key["id"]}"

    return jsonify(response)


@api.route("/quotes/random")
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
    quote = random.choice(dynamodb.get_quotes(start_id=None)[0])
    print(quote)
    response = {"data": quote}
    return jsonify(response)


@api.route("/quotes/<string:quote_id>")
def quote_index(quote_id):
    """Returns a specific quote.
    ---
    parameters:
      - name: quote_id
        in: path
        type: string
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
    try:
        quote = dynamodb.get_quote(quote_id=quote_id)
        response = {"data": quote}
        return jsonify(response)
    except IndexError:
        logging.debug("No quote found")
        return make_response(jsonify(error="Quote not found!"), 404)


@app.errorhandler(404)
def resource_not_found(e):
    return make_response(jsonify(error="Not found!"), 404)


app.register_blueprint(api, url_prefix="/v1")

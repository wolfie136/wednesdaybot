import logging
import os
import random

import boto3
from mastodon import Mastodon

from utils import dynamodb, utils

if logging.getLogger().hasHandlers():
    # The Lambda environment pre-configures a handler logging to stderr. If a handler is already configured,
    # `.basicConfig` does not execute. Thus we set the level directly.
    logging.getLogger().setLevel(logging.INFO)
else:
    logging.basicConfig(level=logging.INFO)


def toot_quote(quote_dict):
    stage = os.getenv("STAGE", "dev")
    client = boto3.client("ssm")
    access_token_parameter = client.get_parameter(
        Name=f"/{stage}/wednesday-api/MASTODON_ACCESS_TOKEN"
    )
    access_token_value = access_token_parameter["Parameter"]["Value"]
    base_url_parameter = client.get_parameter(
        Name=f"/{stage}/wednesday-api/MASTODON_BASE_URL"
    )
    base_url_value = base_url_parameter["Parameter"]["Value"]
    mastodon = Mastodon(
        access_token=access_token_value,
        api_base_url=base_url_value,
    )

    # Toot
    toot_text = quote_dict["text"]
    if "attribution" in quote_dict and quote_dict["attribution"]:
        toot_text = toot_text + " - " + quote_dict["attribution"]

    logging.info(f"Tooting quote: {toot_text}")
    mastodon.status_post(toot_text)
    dynamodb.audit_event(quote_dict["id"], "posted")


def toot_random_quote(event=None, context=None, fake_wednesday=False):
    if utils.is_it_wednesday(fake_wednesday=fake_wednesday):
        quote_list = dynamodb.get_quotes(start_id=None, limit=False)[0]

        posted = False
        while not posted and quote_list:
            random_quote = random.choice(quote_list)
            print(random_quote)
            if not dynamodb.check_quote_posted(random_quote["id"]):
                toot_quote(random_quote)
                posted = True
            else:
                quote_list.remove(random_quote)
        if not posted:
            logging.error("Could not find quote we haven't posted")
    else:
        logging.info("Not tooting because it is not Wednesday")

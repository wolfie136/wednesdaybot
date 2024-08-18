import logging
import os
import random

from mastodon import Mastodon

from utils import utils

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
    if utils.is_it_wednesday():
        random_quote = random.choice(utils.load_quotes())
        toot_quote(random_quote)
    else:
        logging.info("Not tooting because it is not Wednesday")

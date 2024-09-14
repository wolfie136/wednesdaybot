import logging
import os
import random

from mastodon import Mastodon

from utils import dynamodb, utils

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

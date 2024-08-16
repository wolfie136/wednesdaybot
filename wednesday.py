import random
from mastodon import Mastodon
import os

#os.environ.get("MASTODON_ACCESS_TOKEN", "")
#os.environ.get("MASTODON_BASE_URL", "")

mastodon = Mastodon(
    access_token = os.environ.get("MASTODON_ACCESS_TOKEN", ""),
    api_base_url = os.environ.get("MASTODON_BASE_URL", "")
)

lines = open('wednesday.txt').read().splitlines()
quote = random.choice(lines)

mastodon.status_post("{0}".format(quote))

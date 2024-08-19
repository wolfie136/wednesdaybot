import csv
import os
from datetime import datetime


def load_quotes():
    # Read in the CSV to a list of dicts
    wednesday_list = []
    with open("wednesday.csv", newline="") as csvfile:
        reader = csv.DictReader(
            csvfile, delimiter=";", fieldnames=["quote", "attribution"]
        )
        for row in reader:
            if not row["attribution"]:
                row["attribution"] = ""
            wednesday_list.append(
                {"quote": row["quote"], "attribution": row["attribution"]}
            )
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

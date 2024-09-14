import datetime
import logging
import os
import uuid

import boto3

from utils.utils import load_quotes_from_csv

dynamodb = boto3.resource(
    "dynamodb",
    region_name="eu-west-2",
)
dynamodb_table_prefix = os.getenv("DYNAMODB_TABLE_PREFIX", "wednesday-api-dev")


def store_quote(quote_text: str, quote_attribution: str):
    table = dynamodb.Table(f"{dynamodb_table_prefix}-quote")
    now = datetime.datetime.now(datetime.timezone.utc)
    quote_id = str(uuid.uuid4())
    response = table.update_item(
        Key={"id": quote_id},
        UpdateExpression="SET quote_text = :quote_text, quote_added = :quote_added, quote_attribution = :quote_attribution",
        ExpressionAttributeValues={
            ":quote_text": quote_text,
            ":quote_added": now.isoformat(),
            ":quote_attribution": quote_attribution,
        },
    )
    audit_event(quote_id=quote_id, event_type="added", event_timestamp=now.isoformat())
    return response


def audit_event(quote_id: str, event_type: str, event_timestamp):
    event_table = dynamodb.Table(f"{dynamodb_table_prefix}-quote-event")
    return event_table.update_item(
        Key={"id": f"{quote_id}-added-{uuid.uuid4()}", "quote_id": quote_id},
        UpdateExpression="SET event_type = :event_type, event_timestamp = :event_timestamp",
        ExpressionAttributeValues={
            ":event_type": event_type,
            ":event_timestamp": event_timestamp,
        },
    )


def get_quotes(start_id: str, limit: bool = True):
    table = dynamodb.Table(f"{dynamodb_table_prefix}-quote")
    if start_id:
        response = table.scan(Limit=50, ExclusiveStartKey={"id": start_id})
    else:
        if limit:
            response = table.scan(Limit=50)
        else:
            response = table.scan()

    response_items = response["Items"]
    last_evaluated_key = (
        response["LastEvaluatedKey"] if "LastEvaluatedKey" in response else None
    )
    quote_list = []
    for quote in response_items:
        quote_list.append(
            {
                "id": quote["id"],
                "added": quote["quote_added"],
                "text": quote["quote_text"],
                "attribution": quote["quote_attribution"],
            }
        )
    return quote_list, last_evaluated_key


def get_quote(quote_id: str):
    table = dynamodb.Table(f"{dynamodb_table_prefix}-quote")
    response = table.get_item(Key={"id": quote_id})
    quote = response["Item"]
    return {
        "id": quote["id"],
        "added": quote["quote_added"],
        "text": quote["quote_text"],
        "attribution": quote["quote_attribution"],
    }


def import_quotes(path="./wednesday.csv"):
    quote_list = load_quotes_from_csv(path=path)
    for quote in quote_list:
        store_quote(quote_text=quote["quote"], quote_attribution=quote["attribution"])
        logging.info(f"Storing quote {quote}")

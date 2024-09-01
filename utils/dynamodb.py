import logging
import uuid
from datetime import datetime

import boto3

from utils.utils import load_quotes_from_csv

dynamodb = boto3.resource(
    "dynamodb",
    region_name="eu-west-2",
)


def store_quote(quote_text: str, quote_attribution: str):
    table = dynamodb.Table("wednesday-api-dev-quote")
    now = datetime.utcnow()
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
    event_table = dynamodb.Table("wednesday-api-dev-quote-event")
    return event_table.update_item(
        Key={"id": f"{quote_id}-added-{uuid.uuid4()}", "quote_id": quote_id},
        UpdateExpression="SET event_type = :event_type, event_timestamp = :event_timestamp",
        ExpressionAttributeValues={
            ":event_type": event_type,
            ":event_timestamp": event_timestamp,
        },
    )


def get_quotes(start_id: str):
    table = dynamodb.Table("wednesday-api-dev-quote")
    if start_id:
        response = table.scan(Limit=50, ExclusiveStartKey={"id": start_id})
    else:
        response = table.scan(Limit=50)
    quote_list = response["Items"]
    last_evaluated_key = (
        response["LastEvaluatedKey"] if "LastEvaluatedKey" in response else None
    )
    return quote_list, last_evaluated_key


def get_quote(quote_id: str):
    table = dynamodb.Table("wednesday-api-dev-quote")
    response = table.get_item(Key={"id": quote_id})
    return response["Items"]


def import_quotes(path="./wednesday.csv"):
    quote_list = load_quotes_from_csv(path=path)
    for quote in quote_list:
        store_quote(quote_text=quote["quote"], quote_attribution=quote["attribution"])
        logging.info(f"Storing quote {quote}")

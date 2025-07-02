import datetime
import logging
import azure.functions as func
from cosmos_utils import get_old_records, delete_record
from blob_utils import upload_record_to_blob

def main(mytimer: func.TimerRequest) -> None:
    logging.info("Billing archiver function started.")
    cutoff = datetime.datetime.utcnow() - datetime.timedelta(days=90)

    records = get_old_records(cutoff)
    for r in records:
        upload_record_to_blob(r)
        delete_record(r['id'], r['partitionKey'])

    logging.info("Billing archiver function completed.")

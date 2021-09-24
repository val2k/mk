import click
import uuid
import logging

from src.backend import download_file, copy_file_data_into_db

logging.basicConfig()
logger = logging.getLogger("events_ingestor")
logger.setLevel(logging.INFO)

@click.command()
@click.option('--year-and-month', default=None)
def process_file(year_and_month: str):
    request_id = uuid.uuid4()
    logger.info("[{}] - Started processing file...".format(request_id))

    download_file(request_id, year_and_month)
    copy_file_data_into_db(request_id)

if __name__ == "__main__":
    process_file()


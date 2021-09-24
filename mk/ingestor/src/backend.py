import logging
import requests

from .db import connect_db
from .constants import (
    BUCKET_ENDPOINT,
    EVENTS_FILENAME
)
from .utils import check_year_and_month

logger = logging.getLogger("events_ingestor")

def download_file(request_id, year_and_month: str = None):
    logger.info(
        "[{}] - Trying to download file from '{}'."
            .format(request_id, year_and_month)
    )
    year_and_month = check_year_and_month(year_and_month)
    file_url: str = BUCKET_ENDPOINT.format(year_and_month, EVENTS_FILENAME)

    try:
        with requests.get(file_url, stream=True) as r:
            r.raise_for_status()
            with open(EVENTS_FILENAME, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192): 
                    f.write(chunk)
    except requests.exceptions.HTTPError as e:
        logger.error(
            "[{}] - It seems that there is no file at given endpoint"
                .format(request_id)
        )
        raise e

    logger.info(
        "[{}] - File downloaded.'{}'."
            .format(request_id, year_and_month)
    )


def copy_file_data_into_db(request_id):
    logger.info(
        "[{}] - Trying to copy file from into database.."
            .format(request_id)
    )
    conn, cursor = connect_db()
    copy_file_into_db_sql = """
       COPY events FROM stdin WITH CSV HEADER
       DELIMITER as ','
       """

    with open(EVENTS_FILENAME, 'r') as f:
        try:
            cursor.copy_expert(sql=copy_file_into_db_sql, file=f)
        except Exception as e:
            logger.error(
                "[{}] Error while copying CSV file to Database: {}"
                    .format(request_id, e)
            )
            conn.rollback()
            raise e
        else:
            conn.commit()
            logger.info(
                "[{}] - File successfully copied into Database."
                    .format(request_id)
            )
        finally:
            cursor.close()
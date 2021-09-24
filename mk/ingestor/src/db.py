import logging
import psycopg2
import sys

from .constants import (
    POSTGRES_DB,
    POSTGRES_HOST,
    POSTGRES_USER,
    POSTGRES_PW
)

logger = logging.getLogger("events_ingestor")

def connect_db():
    try:
        connection = psycopg2.connect(
            database=POSTGRES_DB,
            host=POSTGRES_HOST,
            user=POSTGRES_USER,
            password=POSTGRES_PW
        )
        cursor = connection.cursor()
    except Exception as e:
        logger.error("Error accessing database: {}".format(e))
        sys.exit(1)
    else:
        return connection, cursor
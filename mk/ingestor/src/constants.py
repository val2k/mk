import os

POSTGRES_DB = str(os.environ['POSTGRES_DB']) if 'POSTGRES_DB' in os.environ else 'postgres'
POSTGRES_HOST = str(os.environ['POSTGRES_HOST']) if 'POSTGRES_HOST' in os.environ else 'host.minikube.internal'
POSTGRES_PW = str(os.environ['POSTGRES_PW']) if 'POSTGRES_PW' in os.environ else 'postgres'
POSTGRES_USER = str(os.environ['POSTGRES_USER']) if 'POSTGRES_USER' in os.environ else 'postgres'

BUCKET_ENDPOINT = "http://work-sample-mk.s3.amazonaws.com/{}/{}"
EVENTS_FILENAME = "events.csv"

YEAR_AND_MONTH_REGEX = "2\d{3}\/\d{2}"
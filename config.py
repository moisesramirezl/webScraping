import os
from google.cloud import secretmanager

PROJECT_ID = "1033385642776"
DATA_BACKEND = "cloudsql"
CLOUDSQL_DATABASE = "data"
CLOUDSQL_CONNECTION_NAME = "trade-278014:southamerica-east1:historical-nemos"
SQLALCHEMY_TRACK_MODIFICATIONS = False

secrets = secretmanager.SecretManagerServiceClient()

CLOUDSQL_USER = secrets.access_secret_version(
    "projects/"+PROJECT_ID+"/secrets/trade-web-scraping-db-user/versions/1").payload.data.decode("utf-8")
CLOUDSQL_PASSWORD = secrets.access_secret_version(
    "projects/"+PROJECT_ID+"/secrets/trade-web-scraping-db-user-password/versions/1").payload.data.decode("utf-8")


# To use cloud proxy to GCP for local development
LOCAL_SQLALCHEMY_DATABASE_URI = (
    'mysql+pymysql://{user}:{password}@localhost/{database}').format(
        user=CLOUDSQL_USER, password=CLOUDSQL_PASSWORD,
        database=CLOUDSQL_DATABASE)

# App Engine needs a unix socket is used to connect to the cloudsql
# instance.
LIVE_SQLALCHEMY_DATABASE_URI = (
    'mysql+pymysql://{user}:{password}@localhost/{database}'
    '?unix_socket=/cloudsql/{connection_name}').format(
        user=CLOUDSQL_USER, password=CLOUDSQL_PASSWORD,
        database=CLOUDSQL_DATABASE, connection_name=CLOUDSQL_CONNECTION_NAME)

if os.environ.get('GAE_INSTANCE'):
    SQLALCHEMY_DATABASE_URI = LIVE_SQLALCHEMY_DATABASE_URI
else:
    SQLALCHEMY_DATABASE_URI = LOCAL_SQLALCHEMY_DATABASE_URI

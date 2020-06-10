# webScraping

## Usage

### start email server

```bash
sudo python3 -m smtpd -c DebuggingServer -n localhost:1025
```

### Config a database

You have 2 options for local development

#### Sqlite database
```bash
rm persistence/site.db && python persistence/nemos.py
```

#### Cloud database using a local proxy
Go to you config.py file and un uncomment this 4 lines

```
#LOCAL_SQLALCHEMY_DATABASE_URI = (
#    'mysql+pymysql://{user}:{password}@localhost/{database}').format(
#        user=CLOUDSQL_USER, password=CLOUDSQL_PASSWORD,
#        database=CLOUDSQL_DATABASE)
```

Install the Cloud SQL Proxy

###### Linux 64
* wget https://dl.google.com/cloudsql/cloud_sql_proxy.linux.amd64 -O cloud_sql_proxy
* chmod +x cloud_sql_proxy

###### Mac 64
* curl -o cloud_sql_proxy https://dl.google.com/cloudsql/cloud_sql_proxy.darwin.amd64
* chmod +x cloud_sql_proxy

##### Others

* go to https://cloud.google.com/python/django/appengine?hl=es-419#installingthecloudsqlproxy


And run mysql proxy to GCP DB

```bash
cloud_sql_proxy --instances="trade-278014:southamerica-east1:historical-nemos"=tcp:3306
```

## Contrib

### installing dependencies
```bash
pip install -r requirements.txt
```

### install git hooks
```bash
pre-commit install
```

### configure alert rules

You need to crate a local folder .userConf/tradeAlertRules.json like this:

```
{
  "rules": [
    {
      "nemo": "LTM",
      "purchaseAlertPrice": 820,
      "saleAlertPrice": 1000
    },
    {
      "nemo": "CTM",
      "purchaseAlertPrice": 500,
      "saleAlertPrice": 2000
    }
  ],
  "mailto": "source.moises@gmail.com"
}
```

### create a local sqlite database for nemos
```
python3 persistence/nemos.py
```
Documentación de comandos básicos https://www.sitepoint.com/getting-started-sqlite3-basic-commands/

### execute options
#### p: 1 use proxy, 0 not use proxy. Default 0
#### v: 1 verbose, 0 not verbose. Default 0
```
python3 main.py -p 1|0 -v 1|0
```

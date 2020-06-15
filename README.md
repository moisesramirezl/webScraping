# webScraping

## Usage

### start email server

```bash
sudo python3 -m smtpd -c DebuggingServer -n localhost:1025
```

### Config a database

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

### execute options
#### port: you can pass another if you want

```
flask run --port=8000
```

## Deploy to GCP

### Install SDK Cloud.
https://cloud.google.com/sdk/docs?hl=es-419

#### Configure service account
https://cloud.google.com/sdk/gcloud/reference/auth/activate-service-account

#### Deploy
```bash
gcloud app deploy
```


## TO DO
* Refactor main.py
* Use options proxy and verbose as parameters
* Handle multiples configurations for nemos and notification email
* Catch exception when the request to scraping page fails

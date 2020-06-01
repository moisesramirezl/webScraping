# webScraping

## Usage

### start email server

```bash
sudo python3 -m smtpd -c DebuggingServer -n localhost:1025
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
#### p: 1 use proxy, 0 not use proxy. Default 0
#### v: 1 verbose, 0 not verbose. Default 0
```
python3 main.py -p 1|0 -v 1|0
```

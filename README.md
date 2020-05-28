# webScraping

## Usage

### start email server
```bash
sudo python3 -m smtpd -c DebuggingServer -n localhost:1025
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
### configure alert rules

```
python3 main.py
```
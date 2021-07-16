import requests
import backoff
from datetime import datetime

class Currency: # from api_module

    BASE_URL = "https://economia.awesomeapi.com.br/json/"

    def __init__(self):
        self.LAST_URL = self.BASE_URL + "last/"
        return

    @backoff.on_exception(
        backoff.expo,
        (ConnectionAbortedError, ConnectionRefusedError, TimeoutError),
        max_tries=5,
    )
    def get_relation(self, exchange):
        url = self.LAST_URL + exchange
        req = requests.get(url)
        return float(req.json()[exchange.replace('-', '')]["bid"])

exchange = 'USD-BRL'
c = Currency()
with open(f'{exchange}.csv', 'a') as f:
    val = c.get_relation(exchange)
    print(f'{exchange}: {val:,.2f}')
    f.write('{};{}'.format(datetime.today(), val))
import logging # SET LOGGING

log = logging.getLogger()
log.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch = logging.StreamHandler()
ch.setFormatter(formatter)
log.addHandler(ch)

import backoff
import requests


class Currency:

    BASE_URL = 'https://economia.awesomeapi.com.br/json/last'

    def __init__(self):
        self.LAST_URL = self.BASE_URL + 'last/'
        return

    @backoff.on_exception(
        backoff.expo, 
        (ConnectionAbortedError, ConnectionRefusedError, TimeoutError), 
        max_tries = 5
    )
    def get_relation(self, c1, c2):
        url = self.LAST_URL + c1 + '-' + c2
        req = requests.get(url)
        return float(req.json()[c1 + c2]['bid'])

if __name__ == '__main__':
    c = Currency()
    print(c.get_relation('USD', 'BRL'))

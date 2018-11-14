import requests
import json


class QuoteAPI:
    URL_FORMAT = "https://talaikis.com/api/quotes/random/"

    @property
    def url(self):
        return self.URL_FORMAT

    def get(self):
        response = requests.get(self.url)
        data = response.json()
        return {'statement': data['quote'], 'author': data['author']}

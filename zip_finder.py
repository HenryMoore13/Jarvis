import requests
import json

secrets = json.load(open("secrets.json"))


class ZipFinderAPI:
    DEFAULT_ZIPCODE = secrets['WeatherInfo']['ZIP_Code']
    URL_FORMAT = "https://www.zipcodeapi.com/rest/" + secrets[
        'ZIP_CodeFinder']['ZipAPI_Key'] + "/info.json/{zipcode}/degrees"

    def __init__(self, zipcode=None):
        self.zipcode = zipcode or self.DEFAULT_ZIPCODE

    @property
    def url(self):
        return self.URL_FORMAT.format(zipcode=self.zipcode)

    def get(self):
        response = requests.get(self.url)
        data = response.json()
        return ZipInfo(city_info={
            'city': data['city'],
            'state': data['state']
        })


class ZipInfo:
    def __init__(self, *, city_info):
        self.city_info = city_info

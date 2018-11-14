import requests
import json

secrets = json.load(open("secrets.json"))


class NewsAPI:
    DEFAULT_COUNTRY = secrets['NewsInfo']['country']
    URL_FORMAT = "https://newsapi.org/v2/top-headlines?pageSize=4&country={country}&apiKey=" + secrets[
        'NewsInfo']['NewsAPI_Key']

    def __init__(self, country=None):
        self.country = country or self.DEFAULT_COUNTRY

    @property
    def url(self):
        return self.URL_FORMAT.format(country=self.country)

    def get(self):
        response = requests.get(self.url)
        data = response.json()
        return News(articles=[{
                'headline': data['articles'][0]['title'],
                'image_URL': check_for_image(data, 0),
                'link': data['articles'][0]['url']
            },{
                'headline': data['articles'][1]['title'],
                'image_URL': check_for_image(data, 1),
                'link': data['articles'][1]['url']
            },{
                'headline': data['articles'][2]['title'],
                'image_URL': check_for_image(data, 2),
                'link': data['articles'][2]['url']
            },{
                'headline': data['articles'][3]['title'],
                'image_URL': check_for_image(data, 3),
                'link': data['articles'][3]['url']
            }])


class News:
    def __init__(self, *, articles):
        self.articles = articles


def check_for_image(data, num):
    if data['articles'][num]['urlToImage'] == None:
        return "https://image.flaticon.com/icons/svg/1199/1199586.svg"
    else:
        return data['articles'][num]['urlToImage']

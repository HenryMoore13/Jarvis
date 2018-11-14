import weather as w
import news as n
import quote as q
import zip_finder as z
import json
from flask import Flask, render_template

secrets = json.load(open("secrets.json"))

app = Flask(__name__)

weather = w.WeatherAPI().get()
news = n.NewsAPI().get()
quote = q.QuoteAPI().get()
zipcode = z.ZipFinderAPI().get()


def cli_main():
    print(show_message())


@app.route("/")
def web_main():
    return render_template(
        'root.html',
        context={
            'userName': secrets['UserInfo']['name'],
            'weather': weather.weather,
            'temp': weather.temp_f,
            'temp_min': weather.min_temp_f,
            'temp_max': weather.max_temp_f,
            'weather_image_URL': weather.get_image_URL(),
            'articles': news.articles,
            'quote': quote,
            'city': zipcode.city_info['city'],
            'state': zipcode.city_info['state']
        })


if __name__ == '__main__':
    app.run()

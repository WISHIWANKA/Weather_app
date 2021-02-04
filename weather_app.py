from flask import Flask, render_template, request, flash
import requests

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret'


@app.route("/", methods=['GET', 'POST'])
def index():
    status = False
    weather_data = [{'status': status}]
    if request.method == 'GET':
        return render_template('index.html', weather_data=weather_data)

    elif request.method == 'POST':
        city_name = request.form.get('city')
        url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=babfdf0877c365d2c8612e228c772745'
        weather_data_json = requests.get(url.format(city_name)).json()

        if weather_data_json['cod'] != 200:
            error_message = "Something went wrong, try one more time!"
            flash(error_message, 'error')
            return render_template('index.html', weather_data=weather_data)

        weather_data = []
        status = True
        weather_parameters = {
            'city': city_name,
            'temperature': weather_data_json['main']['temp'],
            'description': weather_data_json['weather'][0]['description'],
            'icon': weather_data_json['weather'][0]['icon'],
            'humidity': weather_data_json['main']['humidity'],
            'feels like': weather_data_json['main']['feels_like'],
            'status': status
        }
        weather_data.append(weather_parameters)

        return render_template('index.html', weather_data=weather_data)
    return "hello"


if __name__ == '__main__':
    app.run(debug=True)

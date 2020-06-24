from flask import Flask, render_template, request
import requests
import time

app = Flask(__name__)


@app.route('/')
def render_main():
    """render start page"""
    return render_template('main.html')


@app.route('/search', methods=["GET"])
def show_current_weather():
    """ connect with API from openweather and get
     current weather  for chosen by user City"""

    city_name = request.form.get("city")
    data = requests.get(
        f"http://api.openweathermap.org/data/2.5/weather?q={city_name}"
        f"&appid=dfce6593bf021b63c0f93c369d4ad310&units=metric")

    if data.status_code != 200:
        return f"No Data availaible. Received HTTP code {data.status_code}"
    weather_data = data.json()

    current_weather = {'temperature': weather_data.get("main").get('temp'),
                       'feels_like': weather_data.get("main").get('feels_like'),
                       'pressure': weather_data.get("main").get('pressure'),
                       'humidity': weather_data.get("main").get('humidity'),
                       'wind': weather_data.get("wind").get("speed"),
                       }

    return render_template('main.html',
                           weather=current_weather)


@app.route('/main', methods=["GET"])
def generate_forecast_weather ():
    """ extracts data for forecasting weather based on longitude and latitude  from API for current weather"""
    city_name = request.form.get("get_city")
    parameters = requests.get(
        f"http://api.openweathermap.org/data/2.5/weather?q={city_name}"
        f"&appid=dfce6593bf021b63c0f93c369d4ad310&units=metric")

    if parameters.status_code != 200:
        return f"No Data availaible. Received HTTP code {parameters.status_code}"

    parameters_data = parameters.json()
    longtitude = parameters_data.get("coord").get("lon")
    latitude = parameters_data.get("coord").get("lat")

    get_data = requests.get(f'https://api.openweathermap.org/data/2.5/onecall?lat={latitude}&lon={longtitude}'
                            f'&%20exclude=&appid=dfce6593bf021b63c0f93c369d4ad310&units=metric')

    if get_data.status_code != 200:
        return f"No Data availaible. Received HTTP code {get_data.status_code}"

    weather_data = get_data.json()

    """ for daily in weather_data["daily"]:
        for key, value in daily.items():
            if key == 'dt' or key == 'sunrise' or key == 'sunset':
                daily[key] = datetime.datetime.strptime(str(datetime.datetime.fromtimestamp(daily[key])),
                                                        "%Y-%m-%d %H:%M:%S")"""
    weather_data = get_data.json()
    forecast_weather = []
    for i in range(7):
        daily_forecast = {'Date': time.ctime(weather_data["daily"][i]['dt']),
                          'Sunrise': time.ctime(weather_data["daily"][i]['sunrise']),
                          'Sunset': time.ctime(weather_data["daily"][i]['sunset']),
                          'Temperature Day [℃] ': weather_data["daily"][i]['temp']['day'],
                          'Temperature Night [℃]': weather_data["daily"][i]['temp']['night'],
                          'Pressure [hPa]': weather_data["daily"][i]['pressure'],
                          'Humidity [%]': weather_data["daily"][i]['humidity'],
                          'Weather': weather_data["daily"][i]['weather'][0]['main'],
                          'More': weather_data["daily"][i]['weather'][0]['description'],
                          }
        forecast_weather.append(daily_forecast)

    return render_template('main.html',
                           forecast_weather=forecast_weather)


if __name__ == '__main__':
    app.run(debug=True)

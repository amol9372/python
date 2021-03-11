from typing import Tuple
from flask import Flask, json, render_template, request, make_response, jsonify, redirect
import ipinfo
from util import WeatherUtil
from datetime import date, datetime
import calendar

util = WeatherUtil()


class MyFlask(Flask):
    def run(self, host=None, port=None, debug=None, load_dotenv=True, **options):
        # initialize variables
        super(MyFlask, self).run(host=host, port=port,
                                 debug=debug, load_dotenv=load_dotenv, **options)


app = MyFlask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True


@app.route("/", methods = ['POST', 'GET'])
def show_dashboard():
    location_params = request.get_json()
    lat_lng_tuple: Tuple
    google_address: dict = None
    location_data : dict = None
   
    if location_params:
        lat_lng_tuple = (location_params['location']['lat'], location_params['location']['lng'])
        google_address = location_params['address']
    else:
        # Get location from ip address
        user_ip = request.remote_addr
    
        ## check for local IP
        if user_ip == util.local_ip:
            location_data = util.get_location()
        else:
            location_data = util.get_location_from_ip(user_ip)

        lat_lng_tuple = (location_data['latitude'], location_data['longitude'])    
    
    
    address = util.get_address(google_address, location_data)
    # save location data in external file - TODO

    # GET all weather data
    data = util.get_all_weather_data(util.prepare_params(lat_lng_tuple)).json()

    # current_weather(current_temp, main, desc, precipitation, wind, hum)
    # location_data(city, state, region, ZIP)
    # date_time
    # forecast_data(min, max, weather)
    current = data.get("current")
    date_time = util.convert_unix_timestamp_to_datetime(current.get("dt"))
    forecast_data = data.get("daily")
     
    for day in forecast_data:
        # set icons for weather
        day_weather = day.get("weather")
        day_weather[0]["icon"] = util.get_weather_icon(day_weather)
        day["weather"] = day_weather

        # set date time and day of the week
        dt = day.get("dt")
        date_time: datetime = util.convert_unix_timestamp_to_datetime(dt)
        day['dt'] = calendar.day_name[date_time.weekday()]

    # set current weather icon
    current_day_weather = current.get("weather")
    current_day_weather[0]["icon"] = util.get_weather_icon(current_day_weather)
    current["weather"] = current_day_weather

    dt_current = current.get("dt")
    selected_day = calendar.day_name[util.convert_unix_timestamp_to_datetime(dt_current).weekday()]   

    if location_params is not None:
        return render_template("weather_data_search.html", location=address, current_weather=current, 
                                                           date_time=date_time, forecast_data=forecast_data, selected_day = selected_day)

    return render_template("weather_data.html", location=address, current_weather=current, 
                                                           date_time=date_time, forecast_data=forecast_data, selected_day = selected_day)


if __name__ == "__main__":
    app.run()

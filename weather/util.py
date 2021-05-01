from datetime import datetime
from typing import Dict
import requests
import json
import ipinfo
from ssm_parameter_store import EC2ParameterStore

# load configuration data
with open("static/startup.json") as json_file:
    init_data = json.load(json_file)


open_weather_base_params = {"exclude": "minutely,hourly",
                            "units": "metric"}

# get access id and secert from aws to run on local
aws_param_store = EC2ParameterStore(aws_access_key_id="AKIAUU63GJAHLC5EZANZ",
                                    aws_secret_access_key="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",
                                    region_name='ap-south-1')

weather_params = aws_param_store.get_parameters_with_hierarchy(
    "/applications/weather")

print(weather_params)


class WeatherUtil:
    local_ip = "127.0.0.1"

    def __init__(self):
        print("Data has been initialized ::::")

    def get_all_weather_data(self, params: Dict):
        params.update(open_weather_base_params)
        # add api key here
        params.update({"appid": weather_params['openweather_api_key']})
        all_weather_data = requests.get(
            init_data.get("one_call_base_api"), params)
        return all_weather_data

    def get_location_from_ip(self, ip):
        # access_token = init_data.get("ipinfo_token")
        access_token = weather_params['ipinfo_token']
        handler = ipinfo.getHandler(access_token)
        details = handler.getDetails(ip)
        return details.all

    def get_location(self):
        access_token = weather_params['ipinfo_token']
        handler = ipinfo.getHandler(access_token)
        details = handler.getDetails()
        return details.all

    def prepare_params(self, location_tuple):
        params = {"lat": location_tuple[0], "lon": location_tuple[1]}
        return params

    def convert_unix_timestamp_to_datetime(self, timestamp):
        date_time = datetime.fromtimestamp(timestamp)
        return date_time

    def get_address(self, google_address, ipinfo_location):

        address: Dict

        if not google_address:
            address = {"city": ipinfo_location['city'], "state": ipinfo_location['region'],
                       "postal_code": ipinfo_location['postal'], "country": ipinfo_location['country']}
        else:
            address = {"area": google_address.get("sublocality_level_1"), "city": google_address.get("administrative_area_level_2"),
                       "state": google_address.get("administrative_area_level_1"),  "postal_code": google_address.get("postal_code"),
                       "country": google_address.get("country")}
        return address

    def get_weather_icon(self, weather):
        climate_mappings: dict = init_data.get("climate_mappings")
        weather_type = climate_mappings.get(weather[0].get("main"))
        # check if weather decription exists in mappings

        weather_desc = weather[0].get("description")
        if weather_type.get(weather_desc) is not None and weather_type.get(weather_desc) != "":
            return weather_type.get(weather_desc)

        return weather_type.get("default")

# {
#    "id": 800,
#    "main": "Clear", (Rain, Snow, Extreme etc.)
#    "description": "clear sky",
#    "icon": "01d"
# }

# {
#     "base_api": "https://api.openweathermap.org/data/2.5/onecall",
#     "openweather_api_key": "65390ad30b25b0edcb4b5d31cbac5ff0"
#     https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&exclude={}&units={}&appid={}
# }


# {'ip': '2405:201:5005:c186:2d43:acff:b6b4:c02e', 'city':
# 'Mohali', 'region': 'Punjab', 'country': 'IN', 'loc': '30.6800,76.7221',
# 'org': 'AS55836 Reliance Jio Infocomm Limited', 'postal': '140308',
# 'timezone': 'Asia/Kolkata', 'country_name': 'India', 'latitude': '30.6800', 'longitude': '76.7221'}

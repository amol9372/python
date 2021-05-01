import pandas
import folium
import numpy as np
from flask import Flask, render_template, request, make_response, jsonify
from pandas.core.frame import DataFrame
from werkzeug.utils import redirect
from volcano_util import Util

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
data = pandas.read_csv("volcano_data/volcano.csv")
util = Util()


@app.route("/")
def dashboard():
    return render_template("dashboard.html")


@app.route("/volcano")
def volcano():
    print(len(data))
    data2 = data.iloc[0:300]
    map = folium.Map(prefer_canvas=True, location=[
        28.475343, 77.048320], zoom_start=3, tiles="Stamen Terrain")
    fg = folium.FeatureGroup(name="All Volcano_map")
    for index, volcano in data2.iterrows():
        folium.Marker(location=[volcano["latitude"], volcano["longitude"]],
                      popup=volcano["volcano_name"], icon=folium.Icon(color="blue")).add_to(fg)
    map.add_child(fg)
    map.save("static/volcano_map.html")
    return render_template("volcano.html", country=load_state_data(), type=load_type_data())


@app.route("/filter", methods=['POST'])
def filter():
    map = folium.Map(prefer_canvas=True, location=[
        28.475343, 77.048320], zoom_start=3, tiles="Stamen Terrain")

    search_param = list(request.get_json().keys())[0]
    search_value = request.get_json()[search_param]

    query = ""
    if search_param == "elevation":
        query = ("{}" + " {} " + "{}").format(search_param, " > ", search_value)
    else:
        query = ("{}" + " {} " + "'{}'").format(search_param,
                                                " == ", search_value)

    data_filtered = data.query(query)
    fg_filtered = folium.FeatureGroup(name="Filtered Volcano Map")
    for index, volcano in data_filtered.iterrows():
        folium.Marker(location=[volcano["latitude"], volcano["longitude"]],
                      popup=volcano["volcano_name"], icon=folium.Icon(color="blue")).add_to(fg_filtered)

    map.add_child(fg_filtered)
    map.save("static/volcano_map.html")
    return make_response(jsonify({"count": len(data_filtered)}))


@app.route("/search-nearest-volcanoes", methods=["POST"])
def search_nearest_volcanoes():
    lat_lng = request.get_json()["location"]
    radius = int(request.get_json()["radius"])
    nearbuy_volcanoes: list = []
    # iterate over all volcano locations and find nearest ones
    for index, volcano in data.iterrows():
        distance = util.distance_in_km(lat_lng['lat'], lat_lng['lng'],
                                       float(volcano["latitude"]), float(volcano["longitude"]))
        if distance <= radius:
            nearbuy_volcanoes.append(volcano)

    nearbuy_volcanoes_df = DataFrame(nearbuy_volcanoes)
    plot_on_map(nearbuy_volcanoes_df, lat_lng)
    return {"amol": "good boi"}


def plot_on_map(volcanoes, searched_location):
    map = folium.Map(prefer_canvas=True, zoom_start=3, tiles="Stamen Terrain")

    fg_user_searched_location = folium.FeatureGroup(name = "User Searched Location")
    folium.Marker(location=[searched_location['lat'], searched_location['lng']], 
                      popup="My Location", icon=folium.Icon(color="red")).add_to(fg_user_searched_location)

    fg_nearbuy_volcanoes = folium.FeatureGroup(name="Nearbuy Volcano_map")
    for index, volcano in volcanoes.iterrows():
        folium.Marker(location=[volcano["latitude"], volcano["longitude"]],
                      popup=volcano["volcano_name"], icon=folium.Icon(color="blue")).add_to(fg_nearbuy_volcanoes)

    map.add_child(fg_user_searched_location)
    map.add_child(fg_nearbuy_volcanoes)
    map.save("static/volcano_map.html")


@app.route("/show-map")
def show_latest_map():
    return redirect("static/volcano_map.html")


@app.route("/show-map-flask")
def show_map_flask():
    return render_template("embedded_map.html")


def save_map(fg):
    map.add_child(fg)
    map.save("static/volcano_map.html")


def load_state_data():
    return list(np.unique(data["country"]))


def load_type_data():
    return list(np.unique(data["primary_volcano_type"]))


if __name__ == "__main__":
    app.run(debug=True)

import functions

from flask import Flask, render_template, request
from geopy.geocoders import Nominatim

app = Flask(__name__)
@app.route('/')

def index():
    return render_template("index.html")
@app.route('/results', methods=['POST', "GET"])

def results():

    # Defining dictionary of neighborhoods and the API url + APP token.

    neighborhoods_dict = {"Cherry Hill": (47.6090, -122.3086), "South Lake Union": (47.6246, -122.3343),
                          "Uptown": (47.6246, -122.3567), "Ballard Locks": (47.6655043, -122.3971838),
                          "Ballard": (47.6792, -122.3860), "SODO": (47.5798, -122.3276),
                          "Pioneer Square": (47.6017, -122.3320), "University District": (47.6631, -122.3143),
                          "Commercial Core": (47.6, -122.3), "First Hill": (47.6094, -122.3251),
                          "Fremont": (47.6567, -122.3474), "Capitol Hill": (47.6243, -122.3210),
                          "Westlake": (47.6325, -122.3409), "Pike-Pine": (47.6138, -122.3195),
                          "Uptown Triangle": (47.6205, -122.3493), "Belltown": (47.6148, -122.3470),
                          "Ballard": (47.6792, -122.3860), "Greenlake": (47.6797, -122.3256),
                          "Roosevelt": (47.6831, -122.3176), "Chinatown/ID": (47.59, -122.32),
                          "Denny Triangle": (47.61667, -122.34), "Little Saigon": (47.6, -122.32),
                          "Columbia City": (47.5607, -122.2870), "Dexter": (47.6302, -122.3432),
                          "12th Ave": (47.6302, -122.3432), "Lake City": (47.7193, -122.2953),
                          "West Seattle": (47.5611, -122.3815)}

    # Be sure to input your app token here:

    app_token = ""
    url = "https://data.seattle.gov/api/v3/views/7jzm-ucez/query.json?app_token=" + app_token

    # Getting user inputted information and assigning it to variables to simplify, then running the functions to return top parking spots.

    if request.method == "POST":
        neighborhoods = request.form.getlist('neighborhoods')
        radius = float(request.form.get('radius'))
        address = request.form.get('address')
 #       address_coords = functions.geocode_address(address, lbox=None)
        geolocator = Nominatim(user_agent="homework 6 spozzo")
        address_coords = geolocator.geocode(address)
        address_coords = address_coords.latitude, address_coords.longitude
        top_parking = functions.top_parking(
            functions.parking_dict(url, functions.reduce_parking_dict(neighborhoods_dict, neighborhoods)),
            address_coords, radius)
        return render_template("results.html", value=top_parking, address=address, neighborhoods=neighborhoods,
                               radius=radius)
        #try:


       # except:
       #     return render_template("error.html")
    else:
        return "HTTP " +  str(400) + "(Bad Request): Wrong HTTP method"
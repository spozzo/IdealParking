from geopy.geocoders import Photon
from geopy.distance import geodesic
from geopy.point import Point
import urllib.parse, urllib.request, urllib.error, json

# This function takes an address and the coordinates of the desired location bias, and returns either lat, longitude as a tuple
# or None if no location was found. The geocoder (Photon) uses a bounding box around Seattle, and the location bias
# (the containing neighborhood of the street, or None for the user inputted address) to find matching coordinates.

def geocode_address(street, lbox):
    geolocator = Photon(user_agent="homework 6 spozzo")
    location = geolocator.geocode(street, timeout=None, location_bias = lbox, bbox = [(47.466, -122.442), (47.771, -122.222)])
    if location is not None:
        return location.latitude, location.longitude
    else:
        return None

# This function takes a url and a dictionary of neighborhoods and returns a dictionary of blockfaces, with key-value pairs
# for the containing neighborhood (area), the "parking score" (ratio), and the latitude/longitude (coordinates).
# It cleans up the data by changing the location/address name (originally in the API as unit_desc) to an intersection
# such as [on-street] & [intersecting street], in order to be geocoded.

def parking_dict(url, neighborhoods):
    f = urllib.request.urlopen(url)
    data = json.loads(f.read())
    p_dict = {}
    for block in data:
        if "study_area" in block and block["study_area"] in neighborhoods:
            study_area = block["study_area"]
            if "unitdesc" in block:
                location = block["unitdesc"]
                location_tf = True
            else:
                location_tf = False
            if location in p_dict and location_tf:
                x = len(p_dict[block["unitdesc"]])
                p_dict[location][x] = {}
            else:
                x = 0
                p_dict[location] = {x:{}}
            if "parking_spaces" in block:
                parking_spaces = int(block["parking_spaces"])
            else:
                parking_spaces = 0
            if "total_vehicle_count" in block:
                total_vehicle_count = int(block["total_vehicle_count"])
            else:
                total_vehicle_count = 0
            if location_tf:
                p_dict[location][x] = {"study_area": study_area, "parking_spaces": parking_spaces, "total_vehicle_count": total_vehicle_count}
            if p_dict[location][x] == {}:
                del p_dict[location][x]
            if p_dict[location] == {}:
                del p_dict[location]
    clean_dict = {}
    for location in p_dict:
        area = p_dict[location][list(p_dict[location].keys())[0]]["study_area"]
        if area in neighborhoods:
            count = 0
            total_parking_spaces = 0
            location_old = location
            location = location[:location.find("BETWEEN")] + "&" + location[location.find("BETWEEN") + 7:location.find("AND")]

            for x in p_dict[location_old]:
                if p_dict[location_old][x] != {}:
                    count += p_dict[location_old][x]["total_vehicle_count"]
                    total_parking_spaces += p_dict[location_old][x]["parking_spaces"]

            if total_parking_spaces != 0:
                clean_dict[location] =  {}
                clean_dict[location]["old location"] = location_old
                clean_dict[location]["ratio"] = count / total_parking_spaces
                clean_dict[location]["area"] = area
                lat_long = geocode_address(location, neighborhoods[area])
                if lat_long is not None:
                    clean_dict[location]["coordinates"] = lat_long
                else:
                    del clean_dict[location]
    return clean_dict


# This function takes a dictionary of neighborhoods and coordinates, and a list of neighborhoods to include,
# and returns a cleaned up dictionary with only the desired neighborhoods and their coordinates included.

def reduce_parking_dict(neighborhoods, neighborhoods_included):
    addresses_to_delete = []
    for neighborhood in neighborhoods:
        if neighborhood not in neighborhoods_included:
            addresses_to_delete.append(neighborhood)

    for address in addresses_to_delete:
        del neighborhoods[address]
    return neighborhoods

# This function takes a cleaned up dictionary of parking locations (intersections corresponding to streets) and their
# information, a center_point (the coordinates of the desired address to search around), and a range (the desired
# distance to center_point, where intersections are filtered out if they are not close enough). It returns a list
# of the top 5 parking spots, as tuples with their respective intersections, parking scores, and coordinates. This
# list is sorted by parking score.

def top_parking(p_dict, center_point, range):
    p_list = []
    for address in p_dict:
        if geodesic(Point(center_point), p_dict[address]["coordinates"]).mi <= range:
            p_list.append((p_dict[address]["old location"], p_dict[address]["ratio"], p_dict[address]["coordinates"]))

    sorted_data = sorted(p_list, key=lambda x: x[1])
    return sorted_data[0:5]


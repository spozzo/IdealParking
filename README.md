# Ideal Parking

This program creates an interactive website, where users can input a desired address, range, and neighborhoods, to find the best places to park (paid) in Seattle. The website returns a list of intersections, sorted by their "parking score" (a ratio of the average occupancy on the blockface), with information of their coordinates and parking scores included. 

Each intersection is displayed as its on-street, between two intersecting streets. The coordinates corresponding to each blockface may be ever so slightly off, as they're technically based on the intersection of the on-street with the first intersecting street.

Data from: [City of Seattle Annual Parking Study Data](https://data.seattle.gov/Transportation/Annual-Parking-Study-Data/7jzm-ucez/about_data) and [OpenStreetMap](https://www.openstreetmap.org/#map=5/38.00/-88.15)

Geocoders: 

[Photon](https://github.com/komoot/photon) (API Locations)

[Nominatim](https://nominatim.org) (User inputted addresses)

## APP Token
To use this code, you will need to input your own app token in the app.py file. Fortunately, acquiring the APP Token from the City of Seattle's open data is very easy!

### 1. Making a Tyler Data/SODA3 account
To begin with, you'll need to make an account with SODA3/Tyler Data. Follow these instructions here: [Creating an account](https://support.socrata.com/hc/en-us/articles/115004055807-How-to-Sign-Up-for-a-Tyler-Data-Insights-ID)

Make sure you verify your account!

### 2. Signing in to City of Seattle Open Data
Next, you'll need to sign in to the City of Seattle's Open Data website, using the same Tyler Data account you just created: [Sign in/APP token](https://data.seattle.gov/profile/edit/developer_settings)

Accept the license agreement, and then open the link once again: [Sign in/APP token](https://data.seattle.gov/profile/edit/developer_settings)

### Creating an APP Token, and Adding It to the Program
Click "Create New APP Token", and fill out the information.

Copy this new token into the "APP Token" variable in app.py, and the program should run! 

To test if this new APP Token is working, you can copy it to the end of this URL: https://data.seattle.gov/api/v3/views/7jzm-ucez/query.json?app_token= and test that you have access to the API.
## Issues with Runtime?
Due to the quantity of data this program is parsing through, and limitations on the time I was able to put towards making the data processing as efficient as possible, the runtime is unfortunately a bit slow at times. I did the best that I could towards making the code more efficient, but it's still quite slow. I recommend narrowing down to as few neighborhoods as possible for a quicker runtime.


## Issues with coordinate accuracy?
I tried to make the geocoding process in my code as accurate as possible by limiting it to a bounding box around Seattle, and having the coordinates for each intersection use a location bias set around their container neighborhoods. WIth these parameters, the geocoding process is fairly accurate. However, it might still get a coordinate wrong every so often!

Apologies if you end up encountering any issues with the coordinate accuracy.
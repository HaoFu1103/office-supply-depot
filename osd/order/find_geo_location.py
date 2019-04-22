import googlemaps
import json
# find_geo_location

# TODO: implement the function for calculating the best route
def calculate_best_routes():
    gmaps = googlemaps.Client(key='AIzaSyBCZT-thH-GtdhosGuLzXBrWCCbuLf707A')

    # Geocoding an address
    origin_address = '600 S 9th St, San Jose, CA 95112'
    list_of_dest_addresses = ['387 S 1st St, San Jose, CA 95113', '87 N San Pedro St, San Jose, CA 95110']
    mode = "driving"
    geocode_result = gmaps.distance_matrix(origin_address, list_of_dest_addresses, mode)

    # for x in geocode_result:
    #     print(x)
    # print(geocode_result['rows'])
    # info = geocode_result[0].get('geometry').get('location')

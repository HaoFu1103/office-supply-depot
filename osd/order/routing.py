import googlemaps

def calculate_best_routes(list_addresses):
    gmaps = googlemaps.Client(key='AIzaSyBCZT-thH-GtdhosGuLzXBrWCCbuLf707A')

    origin_address = '1601 Coleman Ave, Santa Clara, CA 95050'
    destination_address = '1601 Coleman Ave, Santa Clara, CA 95050'
    mode_delivery = 'driving'

    # geo = gmaps.geocode(list_addresses[0][1])
    # return geo

    waypoints = []
    # convert the given address to actual address supported by Google Maps
    for i, address in enumerate(list_addresses):
        geocode_result = gmaps.geocode(list_addresses[i][1])
        formatted_address = geocode_result[0]['formatted_address']
        waypoints.append(formatted_address)
        list_addresses[i][1] = formatted_address

    direction_result = gmaps.directions(origin_address, destination_address, mode_delivery, waypoints, optimize_waypoints=True)
    routes = direction_result[0]['legs']

    sorted_address_ids = []
    for i, route in enumerate(routes):
        if i > 0:
            address = route['start_address']
            for curr_address in list_addresses:
                if address == curr_address[1]:
                    sorted_address_ids.append(curr_address[0])

    return sorted_address_ids

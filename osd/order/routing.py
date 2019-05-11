import googlemaps

def calculate_best_routes(list_addresses):
    gmaps = googlemaps.Client(key='AIzaSyBCZT-thH-GtdhosGuLzXBrWCCbuLf707A')

    warehouse1_address = '1601 Coleman Ave, Santa Clara, CA 95050'
    warehouse2_address = '2201 Senter Rd, San Jose, CA 95112'
    origin_address = warehouse1_address

    destination_address = '1601 Coleman Ave, Santa Clara, CA 95050'
    mode_delivery = 'driving'
    startpoint = []
    startpoint.append(warehouse1_address)
    startpoint.append(warehouse2_address)


    waypoints = []
    # convert the given address to actual address supported by Google Maps
    for i, address in enumerate(list_addresses):
        geocode_result = gmaps.geocode(list_addresses[i][1])
        formatted_address = geocode_result[0]['formatted_address']
        waypoints.append(formatted_address)
        list_addresses[i][1] = formatted_address

    waypoints = list(dict.fromkeys(waypoints))

    matrix_of_distance = gmaps.distance_matrix(startpoint, waypoints)

    distances_from_warehouse1 = matrix_of_distance['rows'][0]['elements']
    distances_from_warehouse2 = matrix_of_distance['rows'][1]['elements']
    closer_to_warehouse1 = 0
    closer_to_warehouse2 = 0

    # Calculate which warehouse the driver should start delivery
    for i, distance in enumerate(distances_from_warehouse1):
        if distances_from_warehouse1[i]['distance']['value'] < distances_from_warehouse2[i]['distance']['value']:
            closer_to_warehouse1 += 1
        else:
            closer_to_warehouse2 += 1

    if closer_to_warehouse1 > closer_to_warehouse2:
        origin_address = warehouse1_address
    else:
        origin_address = warehouse2_address

    direction_result = gmaps.directions(origin_address, destination_address, mode_delivery, waypoints, optimize_waypoints=True)

    # This routes contains list of addresses ordered in the most optimal way
    routes = direction_result[0]['legs']

    sorted_address_ids = []
    unique_addresses = set()
    for i, route in enumerate(routes):
        if i > 0:
            address = route['start_address']
            for curr_address in list_addresses:
                if address == curr_address[1] and address not in unique_addresses:
                    sorted_address_ids.append(curr_address[0])
                    unique_addresses.add(address)

    return sorted_address_ids, origin_address

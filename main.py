"""
Author: Jaryab S Khan
"""
import json
from station import Station
from line import Line
from branch import Branch
from prediction import Prediction
from network import Network

from pprint import pprint

path_to_jsons = '/modules/cs940/cw1/lines'

def main():
    tube = Network()

    # Populate all the stations and lines to our network
    lines = ['bakerloo', 'central', 'circle', 'district', 'hammersmith-city', 'jubilee', 'metropolitan', 'northern', 'piccadilly', 'victoria', 'waterloo-city']

    for line in lines:
        file = f'{path_to_jsons}/{line}.json'

        with open(file, 'r') as f:
            obj = json.load(f)

        line_obj = Line(obj['lineId'], obj['lineName'])

        for stop_point_sequence in obj['stopPointSequences']:
            branch = Branch(branch_id=stop_point_sequence['branchId'], next_branch_ids=stop_point_sequence['nextBranchIds'])

            for stop_point in stop_point_sequence['stopPoint']:
                station = Station(stop_point['id'], stop_point['name'], stop_point['lines'], stop_point['zone'], stop_point['lat'], stop_point['lon'])
                branch.add_station(station.station_id)
                
                tube.add_station(station)

            line_obj.add_branch(branch)

        tube.add_line(line_obj)

    # Populate our predictions to our network
    with open(f'/modules/cs940/cw1/arrivals/arrivals-5833611.json', 'r') as f:
        obj = json.load(f)

    for arrival in obj:
        pred = Prediction(
            arrival['vehicleId'],
            arrival['naptanId'],
            arrival['lineId'],
            arrival['platformName'],
            arrival.get('destinationNaptanId', ''),
            arrival['timeToStation'],
            arrival['currentLocation']
        )

        tube.add_prediction(pred)

    # Prelimiary tests (should run successfully after implementing everything in the cw)
    print('----- Next 6 trains arriving at TCR overall ----')
    pprint(tube.next_arrivals_by_station('940GZZLUTCR', k=6))

    print('---- Next 12 trains on the Victoria line ---- ')
    pprint(tube.next_arrivals_by_line('victoria', k=12))

    print('---- Next 8 trains at Green park on piccadilly line ---- ')
    pprint(tube.next_arrivals_by_station_and_line(station_id='940GZZLUGPK', line_id='piccadilly', k=8))

    print('---- Where is train 012 on the District line going next? (in order) ---- ')
    # note that you might not have a train 012 in the district line in your arrivals.json - change this accordingly.
    pprint(tube.next_stations_by_train(vehicle_id='012', line_id='district', k=10))


if __name__ == '__main__':
    main()

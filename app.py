import argparse
import csv
import os

import googlemaps

parser = argparse.ArgumentParser()

parser.add_argument('--google_key', help='Google API key',
                    default='AIzaSyCGVAGPRW_4-4YFl3y_xFBQWWGyOPbSxTU')
parser.add_argument('--csv', required=True,
                    help='Local or absolute path to CSV')
parser.add_argument('--report', required=False, choices=('console', 'csv'),
                    help='Report', default='console')

params = parser.parse_args()


def main(params):
    if params.csv is None and params.coordinates is None:
        print('Enter any params please')
        return None

    if not os.path.isfile(params.csv):
        print('CSV "{}" file does not exist'.format(params.csv))
        return None

    client = googlemaps.Client(key=params.google_key)
    csv_results = []
    with open(params.csv, 'r') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            coordinates = float(row['latitude']), float(row['longitude'])
            result = client.reverse_geocode(
                coordinates, result_type='street_address', language='en'
            )
            if len(result) == 0:
                if params.report == 'console':
                    print('%10f %10f %s' % (
                        float(row['latitude']),
                        float(row['longitude']),
                        'Not found'
                    ))
                else:
                    csv_results.append(dict(row, address='Not found'))
                continue
            if params.report == 'console':
                print('%10f %10f %s' % (
                    float(row['latitude']),
                    float(row['longitude']),
                    result[0].get('formatted_address')
                ))
            else:
                csv_results.append(dict(
                    row, address=result[0].get('formatted_address')
                ))
        if len(csv_results) > 0:
            with open('report.csv', 'w') as csv_report:
                writer = csv.DictWriter(csv_report, fieldnames=[
                    'latitude', 'longitude', 'address'
                ])
                writer.writeheader()
                for line in csv_results:
                    writer.writerow(line)


if __name__ == '__main__':
    main(params)

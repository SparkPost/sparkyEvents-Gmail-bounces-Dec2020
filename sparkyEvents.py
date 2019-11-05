#!/usr/bin/env python3
from __future__ import print_function
from datetime import datetime
import configparser, argparse, time, sys, os, csv, requests

def iso8601_tzoffset(timestamp):
    """
    Validate SparkPost Events (https://developers.sparkpost.com/api/events/) time string, which now includes Seconds and (optional) timezone offset.

    :param timestamp: str
    :return: datetime
    """
    format_string = '%Y-%m-%dT%H:%M:%S%z'
    try:
        d= datetime.strptime(timestamp, format_string)
    except ValueError as e:
        raise argparse.ArgumentTypeError(e)
    return d


def getMessageEvents(url, apiKey, params):
    """
    Get SparkPost message events with specified endpoint URL, API Key, and search params.

    :param url: str
    :param apiKey: str
    :param params:
    :return:
    """
    try:
        T = 60  # Reasonable imeout value for API requests
        h = {'Authorization': apiKey, 'Accept': 'application/json'}

        moreToDo = True
        while moreToDo:
            response = requests.get(url, timeout=T, headers=h, params=params)

            # Handle possible 'too many requests' error inside this module
            if response.status_code == 200:
                return response.json()
            elif (response.status_code == 429 and response.json()['errors'][0]['message'] == 'Too many requests') or \
                 (response.status_code == 502 and response.json()['errors'][0]['message'] == 'Could not proceed (502 error)'):
                snooze = 30
                print(response.json(), '.. pausing', snooze, 'seconds for rate-limiting')
                time.sleep(snooze)
                continue                # try again
            else:
                print('Error:', response.status_code, ':', response.text)
                return None

    except ConnectionError as err:
        print('error code', err)
        exit(1)


# -----------------------------------------------------------------------------------------
# Main code
# -----------------------------------------------------------------------------------------
# Get parameters from .ini file
configFile = 'sparkpost.ini'
config = configparser.ConfigParser()
config.read_file(open(configFile))
cfg = config['SparkPost']
apiKey = cfg.get('Authorization', '')           # API key is mandatory
if not apiKey:
    print('Error: missing Authorization line in ' + configFile)
    exit(1)
baseUri = 'https://' + cfg.get('Host', 'api.sparkpost.com')

# If events are not specified, defaults to all
events = cfg.get('Events', '')

# If the fields are not specified, default to a basic few
properties = cfg.get('Properties', 'timestamp,type')
properties = properties.replace('\r', '').replace('\n', '')  # Strip newline and CR
fList = properties.split(',')

# If not specified, default to UTC
parser = argparse.ArgumentParser(
    description='Simple command-line tool to retrieve SparkPost message events into a .CSV file.',
    epilog='SparkPost API key, host, record event type(s) and properties are specified in {}.'.format(configFile))
parser.add_argument('outfile', metavar='outfile.csv', type=argparse.FileType('w'),
                    help='output filename (CSV format), must be writeable.')
parser.add_argument('from_time', type=iso8601_tzoffset,
                    help='Datetime in format of YYYY-MM-DDTHH:MM:ssZ, inclusive.')
parser.add_argument('to_time', type=iso8601_tzoffset,
                    help='Datetime in format of YYYY-MM-DDTHH:MM:ssZ, exclusive.')
args = parser.parse_args()
fh = csv.DictWriter(args.outfile, fieldnames=fList, restval='', extrasaction='ignore')
fh.writeheader()
print('SparkPost events from {} to {}, writing to {}'.format(args.from_time, args.to_time, args.outfile.name))
print('Events:     ', events if events else '<all>')
print('Properties: ', fList)
morePages = True
eventPage = 1
url = baseUri + '/api/v1/events/message'
p = {
    'cursor': 'initial',
    'per_page': 10000,
    'from': args.from_time,
    'to': args.to_time,
}
if events:
    p['events'] = events

while morePages:
    # Measure time for each processing iteration
    startT = time.time()
    res = getMessageEvents(url=url, apiKey=apiKey, params=p)
    if not res:                                 # Unexpected error - quit
        exit(1)
    for i in res['results']:
        # Write out results as CSV rows in the output file
        fh.writerow(i)
    endT = time.time()

    if eventPage == 1:
        print('Total events to fetch: ', res['total_count'])
    print('Page {0:6d}: got {1:6d} events in {2:2.3f} seconds'.format(
        eventPage, len(res['results']), endT - startT))

    # Get the links from the response.  If there is a 'next' link, we continue processing
    if 'links' in res and 'next' in res['links']:
        eventPage += 1
        url = baseUri + res['links']['next']
        p = None                                 # All new params are in the returned "next" url
    else:
        morePages = False
''' A script for monitoring hashrate and other stats\
     from the eth-x.digger.ws JSON API. '''

# Author: Ryan Stenmark <ryanpstenmark@gmail.com>

import requests as req
import json as js
from io import StringIO
import sys
import time

__VERSION__ = 'v0.2.2'


class Shepherd(object):
    interval = 0
    hashrateShortAvg = 0
    hashrateLongAvg = 0
    roundShares = 0
    apiAddress = ""
    json = ""

    def __init__(self):
        ''' Read configuration values '''
        with open("config", 'r') as config:
            self.apiAddress = config.readline()[11:-1]
            self.interval = int(config.readline()[9:-1])

        ''' MOTD '''
        print("Shepherd", __VERSION__, "<ryanpstenmark@gmail.com>\n\
Donate: 0x32F73971Ff64Eb8e4598a1875d443DE8f2Ba924f\n")

        # Main loop
        while(True):
            try:
                # Request JSON from API.
                if self.getJSON() == 1:
                    print("Could not fetch JSON from host")
                    time.sleep(5)
                else:
                    # Scrape stats from JSON API response
                    self.getMiningStats()

                    # Quick reference bar
                    bar = ""
                    for i in range(int(self.roundShares*20)):
                        bar += u"\u2588"

                    # Statistics output
                    print("3h avg:", round(self.hashrateLongAvg/pow(10, 6), 1), "MH/s",
                          "\t30m avg:", round(self.hashrateShortAvg/pow(10, 6), 1), "MH/s",
                          "\tRound share (last 1000 shares):", str(self.roundShares) + "%", bar)
                    time.sleep(self.interval)

            # Exit cleanly on ctl-c '''
            except KeyboardInterrupt:
                sys.exit(0)

    def getJSON(self):
        ''' Make a request to the API endpoint and refresh our data.\
        Return a 0 on success, otherwise return 1. '''
        try:
            response = req.get(self.apiAddress, timeout=self.interval, headers={'user-agent': 'Shepherd/ryanpstenmark@gmail.com'})
            # Raise HTTPError on bad status code
            response.raise_for_status()
            self.json = response.json()
            # Got bad HTTP status code from API.
        except req.HTTPError:
            print("HTTPError exception: bad status code", file=sys.stderr)
            return 1
        # Generic connection error.
        except req.ConnectionError:
            print("ConnectionError exception: are you connected to the internet?", file=sys.stderr)
            return 1
        # Request timed out.
        except req.Timeout:
            print("Timeout exception: Request timed out.", file=sys.stderr)
            return 1
        # Failure to decode JSON response.
        except js.JSONDecodeError:
            print("JSONDecodeError exception", file=sys.stderr)
            return 1
        else:
            return 0

    def getMiningStats(self):
        ''' Utility function for scraping stats from JSON API response. '''
        # Your 30 minute short average (estimated) hashrate.
        self.hashrateShortAvg = self.json['currentHashrate']
        # Your 3 hour long average (estimated) hashrate.
        self.hashrateLongAvg = self.json['hashrate']
        # Your percent contribution to the last 1000 shares found.
        self.roundShares = self.json['roundShares'] / 10


if __name__ == '__main__':
    Shepherd()

#!/usr/bin/env python

import datetime
import os

from owm.owmfetcher import OWMFetcher
# from tts.tts import TTSConverter


def print_weather_data(observation):
    print("-------------------------------------------------------------")
    print(" Weather query at {} returned:".format(datetime.datetime.now()))
    print("   Last observation: {}".format(observation.get_reference_time(timeformat='iso')))
    print("   Temperature: {}".format(observation.get_temperature(unit='celsius')))
    print("   Cloud coverage: {}".format(observation.get_clouds()))
    print("   Rain: {}".format(observation.get_rain()))
    print("   Humidity: {}".format(observation.get_humidity()))
    print("   Detailed status: {}".format(observation.get_detailed_status()))
    print("-------------------------------------------------------------\n")

relative_path_to_key = "../OWM.txt"
current_dir = os.path.dirname(__file__)
key_path = os.path.join(current_dir, relative_path_to_key)

owm_fetcher = OWMFetcher(key_path)
weather = owm_fetcher.get_current_weather()
print_weather_data(weather)

# tts_converter = TTSConverter()
# tts_converter.say(weather.get_detailed_status())

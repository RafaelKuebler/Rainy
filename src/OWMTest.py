#!/usr/bin/env python

import os
import datetime
from owm.owmfetcher import OWMFetcher
from tts.tts import TTSConverter


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

tts_converter = TTSConverter("../audio/")

relative_path_to_key = "../OWM.txt"
current_dir = os.path.dirname(__file__)
key_path = os.path.join(current_dir, relative_path_to_key)

owm_fetcher = OWMFetcher(key_path)
weather = owm_fetcher.get_current_weather()
print_weather_data(weather)

tts_converter.say(weather.get_detailed_status())
tts_converter.say(weather.get_detailed_status())

forecast = owm_fetcher.get_weather_next_3_hours()
print(forecast.get_reception_time('iso'))
print(len(forecast))

print("\nFinished happily! :)")

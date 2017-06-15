class OWMInterpreter:
    def __init__(self, config_path):
        # load preferences from config_path
        self._temp_limit_min = 15

    def interpret_weather(self, weather_observation):
        temperature = weather_observation.get_temperature(unit='celsius')

        rain = weather_observation.get_rain()
        need_umbrella = len(rain) > 0

        temp_min = temperature['temp_min']
        need_jacket = temp_min < self._temp_limit_min

        return {'umbrella': need_umbrella, 'jacket': need_jacket}

    @staticmethod
    def string_weather_data(observation):
        return \
            "-------------------------------------------------------------\n" + \
            "Weather query returned:\n" + \
            "  Last observation: {}\n".format(observation.get_reference_time(timeformat='iso')) + \
            "  Temperature: {}\n".format(observation.get_temperature(unit='celsius')) + \
            "  Cloud coverage: {}\n".format(observation.get_clouds()) + \
            "  Rain: {}\n".format(observation.get_rain()) + \
            "  Humidity: {}\n".format(observation.get_humidity()) + \
            "  Detailed status: {}\n".format(observation.get_detailed_status()) + \
            "-------------------------------------------------------------"

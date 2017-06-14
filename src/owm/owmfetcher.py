import pyowm


class OWMFetcher:
    """Fetch the weather forecasts from OpenWeatherMap.

    Attributes:
        _key (string): OpenWeatherMap API key
        _owm (OWM25): OpenWeatherMap object
        _default_lat (float): Default latitude (Karlsruhe, Germany)
        _default_lon (float): Default longitude (Karlsruhe, Germany)
    """
    _default_lat = 49.01
    _default_lon = 8.42

    def __init__(self, path_to_owm_key="/OWM.txt", language='en'):
        """Initialize OpenWeatherMap objects using the API key.

        Args:
            path_to_owm_key (string): Path to the .txt file containing the API key.
        """
        self._key = self.__read_owm_key_from(path_to_owm_key)
        self._owm = pyowm.OWM(API_key=self._key, language=language)
        print(type(self._owm))

    @staticmethod
    def __read_owm_key_from(path_to_owm_key):
        """Read the OpenWeatherMap key from the specified path.

        Attributes:
            path_to_owm_key (string): Path to the .txt file containing the API key.
        """
        key_file = open(path_to_owm_key, 'r')
        key = key_file.readline()
        key_file.close()

        return key

    def get_current_weather(self, lat=None, lon=None):
        if lat is None or lon is None:
            lat = self._default_lat
            lon = self._default_lon
        # observation = self._owm.weather_at_zip_code('76131', 'DE')
        observation = self._owm.weather_at_coords(lat, lon)
        return observation.get_weather()

    def get_weather_next_3_hours(self, lat=None, lon=None):
        if lat is None or lon is None:
            lat = self._default_lat
            lon = self._default_lon
        forecaster = self._owm.three_hours_forecast_at_coords(lat, lon)
        return forecaster.get_forecast()

    def __str__(self):
        return "OWMFetcher (key: {})".format(self._key)

import pyowm


class OWMFetcher:
    """Fetch the weather forecasts from OpenWeatherMap.

    Attributes:
        _key (string): OpenWeatherMap API key
        _owm (owm): OpenWeatherMap object
    """

    def __init__(self, path_to_owm_key="/OWM.txt", language='en'):
        """Initialize OpenWeatherMap objects using the API key.

        Args:
            path_to_owm_key (string): Path to the .txt file containing the API key.
        """
        self._key = self.__read_owm_key_from(path_to_owm_key)  # API key for OpenWeatherMap
        self._owm = pyowm.OWM(API_key=self._key, language=language)
        print(self)

    @staticmethod
    def __read_owm_key_from(path_to_owm_key):
        """Read the OpenWeatherMap key from the specified path.

        Attributes:
            path_to_owm_key (string): Path to the .txt file containing the API key.
        """
        file = open(path_to_owm_key, 'r')
        key = file.readline()
        file.close()

        return key

    def get_current_weather(self):
        forecast = self._owm.weather_at_zip_code('76131', 'DE')

        return forecast.get_weather()

    def __str__(self):
        return "OWMFetcher (key: {})".format(self._key)

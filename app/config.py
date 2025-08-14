import os
import json
from dotenv import load_dotenv

load_dotenv()


class Config:
    """
    Base configuration class
    """

    # Load environment variables
    URL = os.getenv("URL")
    MAPBOX_API_KEY = os.getenv("MAPBOX_API_KEY")
    USE_HTTPS = (
        os.getenv("USE_HTTPS", "False") == "True"
    )  # USE_HTTPS defaults to False if nothing is provided or if the string is not exactly "True"

    @staticmethod
    def validate_env_vars():
        missing_vars = []

        if not Config.MAPBOX_API_KEY:
            missing_vars.append("MAPBOX_API_KEY")

        if not Config.URL:
            missing_vars.append("URL")

        if missing_vars:
            raise ValueError(
                f"Missing environment variables: {', '.join(missing_vars)}"
            )


def get_config():
    Config.validate_env_vars()
    return Config

import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """
    Base configuration class
    """

    URL = os.getenv("URL")
    MAPBOX_API_KEY = os.getenv("MAPBOX_API_KEY")

    @staticmethod
    def validate_env_vars():
        missing_vars = []

        if not Config.MAPBOX_API_KEY:
            missing_vars.append("MAPBOX_API_KEY")

        if missing_vars:
            raise ValueError(
                f"Missing environment variables: {', '.join(missing_vars)}"
            )


def get_config():
    Config.validate_env_vars()
    return Config

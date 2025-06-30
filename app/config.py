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

    # Load static data
    experience_path = os.path.join(os.path.dirname(__file__), "data", "experience.json")
    with open(experience_path, "r", encoding="utf-8") as f:
        experience_data = json.load(f)

    hobbies_path = os.path.join(os.path.dirname(__file__), "data", "hobbies.json")
    with open(hobbies_path, "r", encoding="utf-8") as f:
        hobbies_data = json.load(f)

    @staticmethod
    def validate_env_vars():
        missing_vars = []

        if not Config.MAPBOX_API_KEY:
            missing_vars.append("MAPBOX_API_KEY")

        if not Config.URL:
            missing_vars.append("URL")

        if not Config.experience_data:
            missing_vars.append("experience_data")

        if not Config.hobbies_data:
            missing_vars.append("hobbies_data")

        if missing_vars:
            raise ValueError(
                f"Missing environment variables: {', '.join(missing_vars)}"
            )


def get_config():
    Config.validate_env_vars()
    return Config

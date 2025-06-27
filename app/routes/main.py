from flask import Blueprint, render_template
from app.config import get_config
import json
import os

main_bp: Blueprint = Blueprint("main", __name__)
config = get_config()


# Cache experience data
experience_path = os.path.join(
    os.path.dirname(__file__), "..", "data", "experience.json"
)
with open(experience_path, "r", encoding="utf-8") as f:
    experience_data = json.load(f)

# Cache hobbies data
hobbies_path = os.path.join(os.path.dirname(__file__), "..", "data", "hobbies.json")
with open(hobbies_path, "r", encoding="utf-8") as f:
    hobbies_data = json.load(f)


@main_bp.route("/")
def index():
    """
    Returns home page
    """
    return render_template(
        "index.html",
        title="Alejandro Villate",
        url=config.URL,
        work_experience=experience_data,
        mapboxgl_pub=config.MAPBOX_API_KEY,
    )


@main_bp.route("/hobbies")
def hobbies():
    """
    Returns hobbies page
    """
    return render_template("hobbies.html", title="Hobbies", hobbies=hobbies_data)

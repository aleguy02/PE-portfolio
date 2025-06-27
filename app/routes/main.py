from flask import Blueprint, render_template
from app.config import get_config
import json
import os

main_bp: Blueprint = Blueprint("main", __name__)
config = get_config()


@main_bp.route("/")
def index():
    """
    Returns home page
    """
    path = os.path.join(os.path.dirname(__file__), "..", "data", "experience.json")
    with open(path, "r", encoding="utf-8") as f:
        work_experience = json.load(f)

    return render_template(
        "index.html",
        title="Alejandro Villate",
        url=config.URL,
        work_experience=work_experience,
        mapboxgl_pub=config.MAPBOX_API_KEY,
    )


@main_bp.route("/hobbies")
def hobbies():
    """
    Returns hobbies page
    """
    path = os.path.join(os.path.dirname(__file__), "..", "data", "hobbies.json")
    with open(path, "r", encoding="utf-8") as f:
        hobbies = json.load(f)

    return render_template("hobbies.html", title="Hobbies", hobbies=hobbies)

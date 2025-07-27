"""
Routes to serve main static pages
"""

from flask import Blueprint, render_template, url_for
import requests
from app.config import get_config

main_bp: Blueprint = Blueprint("main", __name__)
config = get_config()


@main_bp.route("/")
def index():
    """
    Returns home page
    """
    return render_template(
        "index.html",
        title="Alejandro Villate",
        url=config.URL,
        work_experience=config.experience_data,
        mapboxgl_pub=config.MAPBOX_API_KEY,
    )


@main_bp.route("/hobbies")
def hobbies():
    """
    Returns hobbies page
    """
    return render_template("hobbies.html", title="Hobbies", hobbies=config.hobbies_data)


@main_bp.route("/timeline")
def timeline():
    """
    Returns timeline page
    """
    r = requests.get("http://" + config.URL + url_for("api.get_timeline_post"))
    data = r.json()
    return render_template("timeline.html", posts=data["timeline_posts"])

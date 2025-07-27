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
    protocol = "https://" if config.USE_HTTPS else "http://"
    endpoint = url_for("api.get_timeline_post")
    r = requests.get(protocol + config.URL + endpoint)
    data = r.json()
    return render_template("timeline.html", posts=data["timeline_posts"])

"""
Routes to serve main static pages
"""

from flask import Blueprint, render_template, url_for, current_app
import requests

main_bp: Blueprint = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    """
    Returns home page
    """
    return render_template(
        "index.html",
        title="Alejandro Villate",
        url=current_app.config["URL"],
    )


@main_bp.route("/timeline")
def timeline():
    """
    Returns timeline page
    """
    protocol = "https://" if current_app.config["USE_HTTPS"] else "http://"
    endpoint = url_for("api.get_timeline_post")
    r = requests.get(protocol + current_app.config["URL"] + endpoint)
    data = r.json()
    return render_template("timeline.html", posts=data["timeline_posts"])

"""
Routes to serve main static pages
"""

from flask import Blueprint, render_template, url_for, current_app, jsonify
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


@main_bp.route("/health")
def health():
    """
    Healthcheck endpoint for app, nginx, and mysql containers.
    """
    status = {"app": True, "nginx": True, "mysql": False}
    # Nginx check
    try:
        nginx_url = "http://nginx:80/"
        r = requests.get(nginx_url, verify=False, timeout=2)
        status["nginx"] = r.status_code == 200
    except Exception:
        status["nginx"] = False

    # MySQL check
    try:
        endpoint = url_for("api.get_timeline_post")
        r = requests.get("http://" + current_app.config["URL"] + endpoint)
        status["mysql"] = r.status_code == 200
    except Exception:
        status["mysql"] = False

    http_status = 200 if all(status.values()) else 503
    return jsonify(status), http_status

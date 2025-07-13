"""
API routes to interact with MySQL database
"""

from flask import Blueprint, request
from playhouse.shortcuts import model_to_dict
from app.models.timelinepost import TimelinePost

api_bp: Blueprint = Blueprint("api", __name__)


@api_bp.route("/api/timeline_post", methods=["POST"])
def post_timeline_post():
    """
    Create element in TABLE timelinepost
    """
    name = request.form["name"]
    email = request.form["email"]
    content = request.form["content"]
    timeline_post = TimelinePost.create(name=name, email=email, content=content)

    return model_to_dict(timeline_post)


@api_bp.route("/api/timeline_post", methods=["GET"])
def get_timeline_post():
    """
    Fetch all elements in TABLE timelinepost
    """
    return {
        "timeline_posts": [
            model_to_dict(p)
            for p in TimelinePost.select().order_by(TimelinePost.created_at.desc())
        ]
    }


@api_bp.route("/api/timeline_post", methods=["DELETE"])
def pop_timeline_post():
    """
    Pop most recently created element in TABLE timelinepost
    """
    latest_post = (
        TimelinePost.select()
        .order_by(
            TimelinePost.created_at.desc(), TimelinePost.id.desc()
        )  # if two posts were created at the same time, select the one with the higher id
        .limit(1)
        .first()
    )

    if latest_post:
        latest_post.delete_instance()
        return {"deleted": model_to_dict(latest_post)}, 200
    else:
        return {"error": "No posts to delete"}, 404

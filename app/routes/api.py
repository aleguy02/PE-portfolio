"""
API routes to interact with MySQL database
"""

from flask import Blueprint, request
from playhouse.shortcuts import model_to_dict
from app.models.timelinepost import TimelinePost, mydb

api_bp: Blueprint = Blueprint("api", __name__)


@api_bp.before_request
def before_request():
    if mydb.is_closed():
        mydb.connect()


@api_bp.after_request
def after_request(response):
    if not mydb.is_closed():
        mydb.close()
    return response


@api_bp.teardown_request
def teardown_request(exception):
    """
    Ensure database is closed even if an exception occurs
    """
    if not mydb.is_closed():
        mydb.close()


@api_bp.route("/api/timeline_post", methods=["POST"])
def post_timeline_post():
    """
    Create element in TABLE timelinepost
    """
    name = request.form["name"].strip()
    email = request.form["email"].strip()
    content = request.form["content"].strip()

    # Check for duplicate name/email mapping
    existing_with_email = TimelinePost.select().where(TimelinePost.email == email)
    existing_with_name = TimelinePost.select().where(TimelinePost.name == name)

    for post in existing_with_email:
        if post.name != name:
            return {"error": "Email already associated with a different name"}, 400

    for post in existing_with_name:
        if post.email != email:
            return {"error": "Name already associated with a different email"}, 400

    timeline_post = TimelinePost.create(name=name, email=email, content=content)

    return model_to_dict(timeline_post)


@api_bp.route("/api/timeline_post", methods=["GET"])
def get_timeline_post():
    """
    Fetch the 50 most recent elements in TABLE timelinepost
    """
    return {
        "timeline_posts": [
            model_to_dict(p)
            for p in TimelinePost.select()
            .order_by(TimelinePost.created_at.desc())
            .limit(50)
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

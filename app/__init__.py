from flask import Flask, render_template
from app.routes.main import main_bp
from app.routes.api import api_bp
from app.models.timelinepost import init_db


def create_app(test_config=None):
    app = Flask(__name__)

    if test_config:
        app.config.from_mapping(test_config)

    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp)

    @app.errorhandler(404)
    def not_found(e):
        return render_template("404.html", title="Alejandro Villate"), 404

    # Initialize database if not in testing mode
    if not test_config or not test_config.get('TESTING'):
        init_db()

    return app


app = create_app()

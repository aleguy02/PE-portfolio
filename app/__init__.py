from flask import Flask, render_template
from app.routes.main import main_bp
from app.routes.api import api_bp
from app.models.timelinepost import init_db, close_db
from app.config import get_config
import atexit


def create_app(test_config=None):
    app = Flask(__name__)

    if test_config and test_config.get("TESTING"):
        app.config.from_mapping(test_config)
    else:
        init_db()
        atexit.register(close_db)

    config = get_config()
    app.config["URL"] = config.URL
    app.config["USE_HTTPS"] = config.USE_HTTPS

    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp)

    @app.errorhandler(404)
    def not_found(e):
        return render_template("404.html", title="Alejandro Villate"), 404

    return app


app = create_app()

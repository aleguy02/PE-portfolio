from flask import Flask, render_template
from app.routes.main import main_bp


def create_app(test_config=None):
    app = Flask(__name__)

    if test_config:
        app.config.from_mapping(test_config)

    app.register_blueprint(main_bp)

    @app.errorhandler(404)
    def not_found(e):
        return render_template("404.html", title="Alejandro Villate")

    return app


app = create_app()

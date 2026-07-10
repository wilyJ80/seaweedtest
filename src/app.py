from quart import Quart

def create_app():
    app: Quart = Quart(__name__)

    app.url_map.strict_slashes = False

    # Blueprints

    from routes.home_bp import home_bp
    app.register_blueprint(home_bp)

    return app

if __name__ == "__main__":
    app: Quart = create_app()
    app.run()

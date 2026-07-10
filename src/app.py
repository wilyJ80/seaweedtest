from aioboto3.session import Session
from quart import Quart

def create_app():
    app: Quart = Quart(__name__)

    app.url_map.strict_slashes = False

    # Object storage
    session: Session = Session()
    _s3_context = None

    @app.before_serving
    async def startup():
        _s3_context = session.client(
            's3',
            endpoint_url='http://localhost:8333',
            aws_access_key_id='admin',
            aws_secret_access_key='admin123',
            region_name='us-east-1'
        )
        app.config['S3_CLIENT'] = await _s3_context.__aenter__()

    @app.after_serving
    async def shutdown():
        if _s3_context:
            await _s3_context.__aexit__(None, None, None)

    # Blueprints

    from routes.home_bp import home_bp
    app.register_blueprint(home_bp)

    return app

if __name__ == "__main__":
    app: Quart = create_app()
    app.run()

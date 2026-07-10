from aioboto3.session import Session
from quart import Quart

def create_app():
    app: Quart = Quart(__name__)

    app.url_map.strict_slashes = False
    app.secret_key = 'changeme'

    # Object storage
    session: Session = Session()

    @app.before_serving
    async def startup():
        app.config['S3_CONTEXT'] = session.client(
            's3',
            endpoint_url='http://localhost:8333',
            aws_access_key_id='admin',
            aws_secret_access_key='admin123',
            region_name='us-east-1'
        )
        app.config['S3_CLIENT'] = await app.config['S3_CONTEXT'].__aenter__()

    @app.after_serving
    async def shutdown():
        s3_context = app.config['S3_CONTEXT']
        if s3_context:
            await s3_context.__aexit__(None, None, None)

    # Blueprints

    from routes.home_bp import home_bp
    app.register_blueprint(home_bp)

    return app

if __name__ == "__main__":
    app: Quart = create_app()
    app.run()

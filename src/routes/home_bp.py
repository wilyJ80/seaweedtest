from quart import Blueprint, render_template, current_app
from aioboto3.session import Session
from types_aiobotocore_s3.client import S3Client

home_bp = Blueprint("home", __name__)

@home_bp.get('/')
async def home():
    s3: S3Client = current_app.config['S3_CLIENT']

    res = await s3.list_objects(
        Bucket='test'
    )

    objs = [
        {
            "Key": obj['Key'],
            "Size": obj['Size'],
            "LastModified": obj['LastModified'].strftime("%Y-%m-%d")
        }
        for obj in res['Contents']
    ]

    return await render_template('index.html', objs=objs)

@home_bp.route('/object/<key>')
async def get_object_contents(key):
    s3: S3Client = current_app.config['S3_CLIENT']

    obj = await s3.get_object(
        Bucket='test',
        Key=key
    )
    data = await obj['Body'].read()
    return data.decode('utf-8')

from quart import Blueprint, render_template, current_app
from aioboto3.session import Session
from types_aiobotocore_s3.client import S3Client

home_bp = Blueprint("home", __name__)

@home_bp.get('/')
async def home():
    return await render_template('index.html')

@home_bp.route('/get-file')
async def get_file():
    s3: S3Client = current_app.config['S3_CLIENT']

    obj = await s3.get_object(
        Bucket='test',
        Key='hello.txt'
    )
    data = await obj['Body'].read()
    return data.decode('utf-8')

from werkzeug.utils import secure_filename
from quart import Blueprint, render_template, current_app, request, redirect, flash, url_for
from aioboto3.session import Session
from types_aiobotocore_s3.client import S3Client
import mimetypes

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

@home_bp.get('/object/<key>')
async def get_object_contents(key):
    s3: S3Client = current_app.config['S3_CLIENT']

    obj = await s3.get_object(
        Bucket='test',
        Key=key
    )
    data = await obj['Body'].read()
    return data.decode('utf-8')

@home_bp.post('/object/upload')
async def upload_object():
    res = await request.files
    if 'file' not in res:
        # TODO: error redirect: no upload
        pass

    file = res['file']

    if file.filename == '':
        # TODO: error redirect: not file
        pass

    if file:
        filename = secure_filename(file.filename)
        filebytes = file.read()
        content_type, _ = mimetypes.guess_type(filename)
        if not content_type:
            content_type = 'application/octet-stream'

        # TODO: upload
        s3: S3Client = current_app.config['S3_CLIENT']
        await s3.put_object(
            Bucket='test',
            Key=filename,
            Body=filebytes,
            ContentType='text/plain'
        )

        await flash(f'Upload successful: {filename}')
        return redirect(url_for('home.home'))

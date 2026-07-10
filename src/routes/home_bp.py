from quart import Blueprint, render_template

home_bp = Blueprint("home", __name__)

@home_bp.get('/')
async def home():
    return await render_template('index.html')

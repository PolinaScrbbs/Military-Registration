from quart import Blueprint, render_template

index_router = Blueprint("index", __name__)


@index_router.route("/")
async def index():
    return await render_template("index.html", title="Main Page")

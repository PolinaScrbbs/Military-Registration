from quart import Blueprint, render_template

from ..responses import get_news_list

index_router = Blueprint("index", __name__)


@index_router.route("/")
async def index():
    status, news_list = await get_news_list()
    return await render_template("index.html", title="Main Page", news_list=news_list)

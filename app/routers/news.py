from quart import Blueprint, render_template

from ..responses import get_news

news_router = Blueprint("news_router", __name__)


@news_router.route("/news/<int:news_id>")
async def news_details(news_id):
    status, news = await get_news(news_id)
    return await render_template(
        "news_details.html", title=f"News №{news['id']}", news=news
    )

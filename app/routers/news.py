from quart import Blueprint, render_template, request, redirect, url_for, jsonify
from ..responses import get_news, update_news as updt_news, delete_news as dlt_news

news_router = Blueprint("news_router", __name__)


@news_router.route("/news/<int:news_id>")
async def news_details(news_id):
    status, news = await get_news(news_id)
    return await render_template(
        "news_details.html", title=f"News №{news['id']}", news=news
    )


@news_router.route("/update_news/<int:news_id>", methods=["POST", "GET"])
async def update_news(news_id: int):
    error_message = None

    token = request.cookies.get("access_token")
    if not token:
        next_url = request.url
        return redirect(url_for("auth_router.login", next=next_url))

    if request.method == "POST":
        form = await request.form
        title = form.get("title")
        content = form.get("content")

        data = {
            "filename": title,
            "content": content,
        }

        status, response = await updt_news(token, news_id, data)

        if status == 200:
            return redirect(url_for("news_router.news_details", news_id=news_id))
        elif status == 401:
            next_url = request.url
            return redirect(url_for("auth_router.login", next=next_url))
        else:
            error_message = response["detail"]

    _, news = await get_news(news_id)

    context = {
        "title": f"Update News №{news['id']}",
        "news_id": news_id,
        "news": news,
        "error_message": error_message,
    }

    return await render_template("update_news.html", **context)


@news_router.route("/delete_news/<int:news_id>")
async def delete_news(news_id: int):

    token = request.cookies.get("access_token")
    if not token:
        next_url = request.url
        return redirect(url_for("auth_router.login", next=next_url))

    status, response = await dlt_news(token, news_id)
    if status == 200:
        return redirect(url_for("index.index"))
    elif status == 401:
        next_url = request.url
        return redirect(url_for("auth_router.login", next=next_url))
    else:
        error_message = response["detail"]
        return jsonify({"error": error_message}), 400

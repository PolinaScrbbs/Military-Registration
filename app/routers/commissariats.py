from quart import Blueprint, render_template

from ..responses import get_commissariats

commissariats_router = Blueprint("commissariats_router", __name__)


@commissariats_router.route("/commissariats")
async def page():
    _, commissariats = await get_commissariats()
    context = {"title": f"Commissariats", "commissariats": commissariats}
    return await render_template(f"commissariats.html", **context)

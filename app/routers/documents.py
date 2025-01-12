from quart import Blueprint, render_template

from ..responses.documents import get_documents

documents_router = Blueprint("documents_router", __name__)


@documents_router.route("/documents/<category>")
async def page(category: str):
    _, documents = await get_documents(category)
    context = {
        "title": f"{category.replace('_', ' ').capitalize()} Documents",
        "documents": documents,
    }
    return await render_template(f"documents.html", **context)

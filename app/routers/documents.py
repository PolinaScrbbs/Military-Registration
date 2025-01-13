from quart import Blueprint, render_template, request, jsonify

from ..responses import get_documents, get_archived_documents

documents_router = Blueprint("documents_router", __name__)


@documents_router.route("/documents/<category>")
async def page(category: str):
    _, documents = await get_documents(category)
    context = {
        "title": f"{category.replace('_', ' ').capitalize()} Documents",
        "documents": documents,
    }
    return await render_template(f"documents.html", **context)


@documents_router.route("/documents/create/<category>")
async def create_document_form(category: str):
    token = request.cookies.get("access_token")
    if not token:
        return jsonify({"message": "Unauthorized"}), 403


@documents_router.route("/documents/archive")
async def archive():
    _, documents = await get_archived_documents()
    context = {
        "title": "Archive",
        "documents": documents
    }
    return await render_template(f"documents.html", **context)

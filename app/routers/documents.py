from quart import Blueprint, render_template, request, redirect, url_for
from ..responses import (
    get_documents,
    get_archived_documents,
    post_document,
    get_document,
)

documents_router = Blueprint("documents_router", __name__)


@documents_router.route("/documents/<category>")
async def page(category: str):
    _, documents = await get_documents(category)
    context = {
        "title": f"{category.replace('_', ' ').capitalize()} Documents",
        "category": category,
        "documents": documents,
    }
    return await render_template(f"documents.html", **context)


@documents_router.route("/documents/add/<string:category>", methods=["GET", "POST"])
async def add_document(category: str):
    error_message = None

    token = request.cookies.get("access_token")
    if not token:
        next_url = request.url
        return redirect(url_for("auth_router.login", next=next_url))

    if request.method == "POST":
        form = await request.form
        files = await request.files
        filename = form.get("filename")
        uploaded_file = files.get("file")

        if not uploaded_file:
            error_message = "Файл не выбран!"
        else:
            try:
                file_bytes = uploaded_file.read()
                result, error = await post_document(
                    token, filename, category, file_bytes, uploaded_file.filename
                )

                if result:
                    return redirect(url_for("documents_router.page", category=category))
                else:
                    error_message = error.get("detail", "Ошибка загрузки документа")
            except Exception as e:
                error_message = f"Произошла ошибка: {str(e)}"

    return await render_template(
        "add_document.html", category=category, error_message=error_message
    )


@documents_router.route("/documents/archive")
async def archive():
    _, documents = await get_archived_documents()
    context = {"title": "Archive", "documents": documents}
    return await render_template(f"documents.html", **context)


@documents_router.route("/documents/<int:document_id>")
async def document_details(document_id):
    _, response_data = await get_document(document_id)
    return await render_template("document_details.html", document=response_data)

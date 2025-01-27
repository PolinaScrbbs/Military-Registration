from quart import Blueprint, render_template, request, redirect, url_for, jsonify
from ..responses import (
    get_documents,
    get_archived_documents,
    post_document,
    get_document,
    update_document as updt_document,
    get_categories,
    get_category,
    delete_document as dlt_document,
)
from ..utils import get_empty_category_message

documents_router = Blueprint("documents_router", __name__)


@documents_router.route("/documents/<category>")
async def page(category: str):
    _, documents = await get_documents(category)
    empty_category_message = await get_empty_category_message(category)
    context = {
        "title": f"{category.replace('_', ' ').capitalize()} Documents",
        "category": category,
        "empty_category_message": empty_category_message,
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
                status, response = await post_document(
                    token, filename, category, file_bytes, uploaded_file.filename
                )

                if status == 200:
                    return redirect(url_for("documents_router.page", category=category))
                elif status == 401:
                    next_url = request.url
                    return redirect(url_for("auth_router.login", next=next_url))
                else:
                    error_message = response["detail"]

            except Exception as e:
                error_message = f"Произошла ошибка: {str(e)}"

    _, category_value = await get_category(category)
    return await render_template(
        "add_document.html",
        category=category,
        category_value=category_value.lower(),
        error_message=error_message,
    )


@documents_router.route("/documents/archive")
async def archive():
    _, documents = await get_archived_documents()
    context = {
        "title": "Archive",
        "category": "archive",
        "empty_category_message": "Архив пуст",
        "documents": documents,
    }
    return await render_template(f"documents.html", **context)


@documents_router.route("/document/<int:document_id>")
async def document_details(document_id):
    category = request.args.get("category")
    _, document = await get_document(document_id)

    context = {
        "title": document["filename"],
        "category": category,
        "document": document,
    }

    return await render_template("document_details.html", **context)


@documents_router.route("/update/<int:document_id>", methods=["POST", "GET"])
async def update_document(document_id: int):
    error_message = None
    rq_category = request.args.get("category")

    token = request.cookies.get("access_token")
    if not token:
        next_url = request.url
        return redirect(url_for("auth_router.login", next=next_url))

    if request.method == "POST":
        form = await request.form
        filename = form.get("filename")
        category = form.get("category").lower()
        is_archived = form.get("is_archived")

        data = {
            "filename": filename,
            "category": category,
            "is_archived": is_archived if is_archived else False,
        }

        status, response = await updt_document(token, document_id, data)

        if status == 200:
            return redirect(
                url_for(
                    "documents_router.document_details",
                    document_id=document_id,
                    category=rq_category,
                )
            )
        elif status == 401:
            next_url = request.url
            return redirect(url_for("auth_router.login", next=next_url))
        else:
            error_message = response["detail"]

    _, document_response = await get_document(document_id)
    _, categories_response = await get_categories()

    context = {
        "title": "Update Document",
        "document_id": document_id,
        "categories": categories_response,
        "document": document_response,
        "error_message": error_message,
    }

    return await render_template("update_document.html", **context)


@documents_router.route("/delete/<int:document_id>")
async def delete_document(document_id):
    category = request.args.get("category")

    token = request.cookies.get("access_token")
    if not token:
        next_url = request.url
        return redirect(url_for("auth_router.login", next=next_url))

    status, response = await dlt_document(token, document_id)
    if status == 200:
        return redirect(url_for("documents_router.page", category=category))
    elif status == 401:
        next_url = request.url
        return redirect(url_for("auth_router.login", next=next_url))
    else:
        error_message = response["detail"]
        return jsonify({"error": error_message}), 400

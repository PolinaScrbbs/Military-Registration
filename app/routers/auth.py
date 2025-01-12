from quart import Blueprint, render_template, request, jsonify
from quart_jwt_extended import set_access_cookies, create_access_token
import jwt

from ..config import API_SECRET_KEY
from ..responses import login as login_response

auth_router = Blueprint("auth_router", __name__)


@auth_router.route("/login", methods=["GET", "POST"])
async def login():
    if request.method == "POST":
        form = await request.form
        username = form.get("username")
        password = form.get("password")

        status, response_data = await login_response(username, password)

        if status == 200:
            external_token  = response_data["access_token"]
            decoded_token = jwt.decode(external_token, API_SECRET_KEY, algorithms=["HS256"])
            identity = decoded_token.get("sub")

            new_token = create_access_token(identity=identity)

            resp = jsonify(message="Login successful")
            set_access_cookies(resp, new_token)
            return resp

        return "Ошибка авторизации"

    return await render_template("login.html")

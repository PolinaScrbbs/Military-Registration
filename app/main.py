from datetime import timedelta
from quart import Quart
from quart_jwt_extended import JWTManager

from .config import SECRET_KEY, API_SECRET_KEY

from .routers import index_router
from .routers import documents_router
from .routers import commissariats_router
from .routers import auth_router


app = Quart(__name__, static_folder="static", template_folder="templates")

app.config["JWT_SECRET_KEY"] = API_SECRET_KEY
app.config["JWT_ACCESS_COOKIE_NAME"] = "access_token"
app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
app.config["JWT_COOKIE_SECURE"] = False
app.config["JWT_ACCESS_COOKIE_PATH"] = "/"
app.config["JWT_COOKIE_CSRF_PROTECT"] = True

jwt = JWTManager(app)

app.register_blueprint(index_router)
app.register_blueprint(documents_router)
app.register_blueprint(commissariats_router)
app.register_blueprint(auth_router)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=True)

from quart import Quart

from .routers import index_router
from .routers import documents_router


app = Quart(__name__, static_folder="static", template_folder="templates")

app.register_blueprint(index_router)
app.register_blueprint(documents_router)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=True)

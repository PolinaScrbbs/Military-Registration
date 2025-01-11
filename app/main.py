from quart import Quart
from routers import index_router

app = Quart(__name__, static_folder="static", template_folder="templates")

app.register_blueprint(index_router)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=True)
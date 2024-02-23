import json
from chalice import Chalice

app = Chalice(app_name='instagrid')

@app.route("/", methods=["GET", "POST"])
def index():
    if app.current_request.method == "GET":
        return {"message": "Hello"}
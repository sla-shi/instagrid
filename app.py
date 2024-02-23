import json
from chalice import Chalice
from parse import *

app = Chalice(app_name='instagrid')

@app.route("/", methods=["GET", "POST"])
def index():
    if app.current_request.method == "GET":
        return {"message": "Hello"}
    elif app.current_request.method == "POST":
        # Access the device and payload data from the POST request
        device = app.current_request.json_body["device"]
        payload = app.current_request.json_body["payload"]
        log_str = make_log_str(device, parse_binary_data(payload))
        print (log_str, file=sys.stdout)
        # Process the data as needed (e.g., store it, send it elsewhere)
        return {"message": log_str}
    else:
        return {"error": "Unsupported method"}, 405
from flask import request, render_template, Flask
from model.all_hopping_reader import AllHoppingReader

app = Flask(__name__)


@app.route('/')
def index():
    return render_template(
        "index.html"
    )


@app.route("/get_graph", methods=["GET", "POST"])
def get_graph():
    # Create the all hopping reader
    all_hopping_reader = AllHoppingReader(option=request.json)
    return all_hopping_reader.draw_parallel_coordinate()


@app.route('/upload', methods=['POST'])
def upload_file():
    # Get the file from flask.
    file = request.files["file"]
    # Save the file to proper location
    file.save("data/data.xlsx")
    # Return a dummy message to front end.
    return "GOOD"

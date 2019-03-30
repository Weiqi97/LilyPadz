from flask import request, render_template, Flask

from lilypadz.model.data_reader import get_one_hop

app = Flask(
    __name__,
    static_folder="static",
    template_folder="templates"
)


@app.route('/')
def index():
    return render_template(
        "index.html"
    )


@app.route("/get_graph", methods=["POST"])
def get_graph():
    temp = get_one_hop(name="Atlas", hop=5)
    return "Works!"


@app.route('/upload', methods=['POST'])
def upload_file():
    # Get the file from flask.
    file = request.files["file"]
    # Save the file to proper location
    file.save("data/data.csv")
    # Return a dummy message to front end.
    return "GOOD"

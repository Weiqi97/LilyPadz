from flask import Flask, request, render_template

from lilypadz.model.clustering import get_clustering_result
from lilypadz.model.small_series import get_small_series_for_one_toad

# Set up the flask app with desired parameters.
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


@app.route("/small_series", methods=["POST"])
def small_series():
    options = request.json
    # get_clustering_result(n_clusters=2)
    return get_small_series_for_one_toad(
        name=options["toad_selection"],
        variable=options["small_series_variable"].split("!")
    )


@app.route('/upload', methods=['POST'])
def upload_file():
    # Get the file from flask.
    file = request.files["file"]
    # Save the file to proper location
    file.save("data/data.csv")
    # Return a dummy message to front end.
    return "GOOD"

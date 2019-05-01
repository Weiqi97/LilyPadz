from flask import Flask, request, render_template

from lilypadz.model.clustering import get_all_clustering_result, \
    get_one_clustering_result
from lilypadz.model.small_series import get_ss_for_one_toad, \
    get_ss_for_multiple_toads, get_ss_for_one_toad_sight, \
    get_ss_for_multiple_toads_sight

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
    if not options["sight"]:
        if options["compare"]:
            return get_ss_for_multiple_toads(
                names=options["toads"].split("!"),
                variable=options["variable"].split("!")
            )
        else:
            return get_ss_for_one_toad(
                name=options["toad"],
                variable=options["variable"].split("!")
            )
    else:
        if options["compare"]:
            return get_ss_for_multiple_toads_sight(
                names=options["toads"].split("!"),
                variable=options["variable"].split("!")
            )
        else:
            return get_ss_for_one_toad_sight(
                name=options["toad"],
                variable=options["variable"].split("!")
            )


@app.route("/cluster", methods=["POST"])
def cluster():
    options = request.json
    if not options["sight"]:
        if options["compare"]:
            return get_all_clustering_result(
                n_clusters=int(options["num_cluster"]),
                names=options["toads"].split("!"),
                variable=options["variable"].split("!")
            )
        else:
            return get_one_clustering_result(
                n_clusters=int(options["num_cluster"]),
                name=options["toad"],
                variable=options["variable"].split("!")
            )
    else:
        if options["compare"]:
            return get_all_clustering_result(
                n_clusters=int(options["num_cluster"]),
                names=options["toads"].split("!"),
                variable=options["variable"].split("!")
            )
        else:
            return get_one_clustering_result(
                n_clusters=int(options["num_cluster"]),
                name=options["toad"],
                variable=options["variable"].split("!")
            )


@app.route('/upload', methods=['POST'])
def upload_file():
    # Get the file from flask.
    file = request.files["file"]
    # Save the file to proper location
    file.save("lilypadz/data/dummy")
    # Return a dummy message to front end.
    return "GOOD"

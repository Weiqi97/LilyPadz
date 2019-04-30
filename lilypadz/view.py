from flask import Flask, request, render_template
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
    toad_select = options["toad_selection"]
    if not options["sight"]:
        if "!" in toad_select:
            return get_ss_for_multiple_toads(
                names=toad_select.split("!"),
                variable=options["small_series_variable"].split("!")
            )
        else:
            return get_ss_for_one_toad(
                name=options["toad_selection"],
                variable=options["small_series_variable"].split("!")
            )
    else:
        if "!" in toad_select:
            return get_ss_for_multiple_toads_sight(
                names=toad_select.split("!"),
                variable=options["small_series_variable"].split("!")
            )
        else:
            return get_ss_for_one_toad_sight(
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

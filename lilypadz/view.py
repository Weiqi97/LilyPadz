from flask import Flask, request, render_template
from lilypadz.model.small_series import get_small_series

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
    return get_small_series()


@app.route('/upload', methods=['POST'])
def upload_file():
    # Get the file from flask.
    file = request.files["file"]
    # Save the file to proper location
    file.save("data/data.csv")
    # Return a dummy message to front end.
    return "GOOD"

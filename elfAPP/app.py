from flask import Flask, request, render_template, jsonify
from ELF import process_shifts
import os

app = Flask(__name__)



def ensure_dir(directory):
    """
    Ensure that a directory exists. If the directory does not exist, it is created.

    Args:
    directory (str): The path of the directory to check and potentially create.
    """
    if not os.path.exists(directory):
        os.makedirs(directory)


@app.route("/")
def index():
    """
    Route to render the index page.

    Returns:
    Rendered template: The HTML template for the index page.
    """
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():
    """
    Route to handle the upload of CSV files and process them to assign shifts.

    Returns:
    JSON response: A list of dictionaries with shift assignments, or an error message.
    """
    if (
        "shifts_file" not in request.files
        or "available_times_file" not in request.files
        or "exclusion_file" not in request.files
    ):
        return "No selected file", 400

    shifts_file = request.files["shifts_file"]
    available_times_file = request.files["available_times_file"]
    exclusion_file = request.files["exclusion_file"]

    if (
        shifts_file.filename == ""
        or available_times_file.filename == ""
        or exclusion_file.filename == ""
    ):
        return "No selected file", 400

    temp_dir = "temp"
    ensure_dir(temp_dir)

    shifts_file_path = os.path.join(temp_dir, shifts_file.filename)
    available_times_file_path = os.path.join(temp_dir, available_times_file.filename)
    exclusion_file_path = os.path.join(temp_dir, exclusion_file.filename)
    shifts_file.save(shifts_file_path)
    available_times_file.save(available_times_file_path)
    exclusion_file.save(exclusion_file_path)


    result = process_shifts(
        shifts_file_path, exclusion_file_path, available_times_file_path
    )
    result_list = [
        {"Shift": shift, "Assigned Person": person} for shift, person in result.items()
    ]

    os.remove(shifts_file_path)
    os.remove(available_times_file_path)
    os.remove(exclusion_file_path)

    return jsonify(result_list)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)

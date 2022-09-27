# Temporary Flask backend that I will use for now to develop the frontend.
# Once I learn how to use NodeJS and PostgreSQL

from flask import Flask, render_template, send_from_directory, request
from os.path import join, isfile

# Set flask app name and upload folder. This tells flask where the top directory is.
app = Flask(__name__, template_folder="../front-end/")
# In this case, we want the top directory to be the upload directory (this will also function as download)
app.config['UPLOAD_FOLDER'] = "../front-end/"

# For downloading entire files within the flask directories (such as JSON or Shapefile)
@app.route('/<path:filename>', methods=['GET', 'POST'])
def fetch(filename):
    uploads = join(app.root_path, app.config['UPLOAD_FOLDER'])
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# This is the main landing page, what the user sees
@app.route('/')
def main():
    # We use the HTML file as the template
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="localhost", port=8000, debug=True)


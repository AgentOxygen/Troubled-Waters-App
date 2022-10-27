from flask import Flask
from datetime import date

app = Flask(__name__)

@app.route("/")
def hello_world():
    return f"UT-UCS Troubled Waters back-end Flask server: {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}"

if __name__ == "__main__":
    # Port 1024 is open on thunder for most users
    app.run(host="localhost", port=8000, debug=True)


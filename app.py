# import flask
from flask import Flask, render_template

# create a new flask app instance
app = Flask(__name__)

# create route that renders index.html template
@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
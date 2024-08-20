from flask import Flask,render_template

app = Flask(__name__)


@app.route("/")
def index():
    return "Testing 123"



if __name__ in "__main__":
    app.run(debug=True)

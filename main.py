from flask import Flask, render_template

app = Flask(__name__)


@app.route("/generate_cv")
def hello_world():
    return render_template("base.html")


if __name__ == '__main__':
    app.run(debug=True)

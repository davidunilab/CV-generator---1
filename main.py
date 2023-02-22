from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
# import sqlite3

#  sqlachemy
db = SQLAlchemy()
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///cv.db"
app.config["SQALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    surname = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True)




@app.route("/")
def index():
    return render_template("index.html")

@app.route("/generate_cv")
def generate_cv():
    return render_template("generate_cv.html")

@app.route("/experience")
def experience():
    return render_template("experience.html")

@app.route("/preview")
def preview():
    return render_template("preview.html")

 
if __name__ == '__main__':
    # with app.app_context():
    #     db.create_all()
    #     print(f"db created: {db.engine.url}")
    app.run(debug=True)



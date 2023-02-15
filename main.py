from flask import Flask, render_template, request
# import sqlite3

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/generate_cv")
def generate_cv():
    # con = sqlite3.connect("C:\Users\HP\Desktop\UNILAB-PYTHON\Final Project\CV generator - 1\cv_builder.db")
    # cur = con.cursor() 
    # cur.execute("CREATE TABLE users(name, surname, email)")
    # res = cur.execute("select * from users")
    # print(res.fetchone())
    
    # print(request)
    return render_template("generate_cv.html")

@app.route("/preview")
def preview():
    return render_template("preview.html")

 
if __name__ == '__main__':
    app.run(debug=True)

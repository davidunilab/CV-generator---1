from flask import Flask, render_template, request, redirect, url_for
from flask_admin.contrib.sqla import ModelView
from flask_admin.menu import MenuLink
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import StringField, SubmitField, SelectField, PasswordField
from flask_admin import Admin
from wtforms.validators import DataRequired, Email, Length

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///cv.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SECRET_KEY'] = "this_is_secret"
app.config['FLASK_ADMIN_SWATCH'] = "cerulean"

admin = Admin(app, name='CV Generator', template_mode='bootstrap4')
#  SQLAlchemy
db = SQLAlchemy()
db.init_app(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    surname = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String, nullable=False)


class UserView(ModelView):
    can_export = True


admin.add_link(MenuLink(name='Live site', url='/'))
admin.add_view(UserView(User, db.session))


class CreateResume(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    surname = StringField("Surname")
    email = StringField("Email", validators=[DataRequired(), Email()])
    gender = SelectField(
        "Gender",
        choices=[
            ('m', 'Male'),
            ('f', 'Female'),
            ('o', 'Other')
        ],
        validators=[DataRequired()]
    )
    phone = StringField("Phone number")
    address = StringField("Address")
    city = StringField("City")
    country = StringField("Country")
    password = PasswordField("Password", validators=[DataRequired(), Length(min=4, max=20)])

    submit = SubmitField("Submit")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/generate_cv", methods=["GET", "POST"])
def generate_cv():
    form = CreateResume()
    if form.validate_on_submit():  # if form is filled correctly
        # hash password
        form.password.data = generate_password_hash(form.password.data)

        user = User(
            name=form.name.data,
            surname=form.surname.data,
            email=form.email.data,
            password=form.password.data
            # აქ გაგრძელება შეიძლება/უნდა
        )  # crete user object
        db.session.add(user)
        db.session.commit()  # save user object to db
        return redirect(url_for("preview"))
    print(form.errors)  # print errors in console for debugging
    return render_template("generate_cv.html", form=form)


@app.route("/experience")
def experience():
    # redirect to preview
    return redirect(url_for("preview"))


@app.route("/preview")
def preview():
    return render_template("preview.html")


if __name__ == '__main__':
    # with app.app_context():
    #     db.create_all()
    #     print(f"db created: {db.engine.url}")
    app.run(debug=True)

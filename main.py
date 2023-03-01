from flask import Flask, render_template, request, redirect, url_for, session, flash, abort
from flask_admin.contrib.sqla import ModelView
from flask_admin.menu import MenuLink
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import StringField, SubmitField, SelectField, PasswordField
from flask_admin import Admin
from wtforms.validators import DataRequired, Email, Length
from flask_login import LoginManager, login_user, UserMixin, logout_user, current_user

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///cv.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SECRET_KEY'] = "this_is_secret"
app.config['FLASK_ADMIN_SWATCH'] = "cerulean"

admin = Admin(app, name='CV Generator', template_mode='bootstrap4')
#  SQLAlchemy
db = SQLAlchemy()
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    surname = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String, nullable=False)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class UserView(ModelView):
    can_export = True


admin.add_link(MenuLink(name='Live site', url='/'))
admin.add_view(UserView(User, db.session))


class CreateResume(FlaskForm):
    name = StringField("Name", validators=[DataRequired(message="Name is required")])
    surname = StringField("Surname")
    email = StringField("Email", validators=[DataRequired(message="Email is required"), Email()])
    gender = SelectField(
        "Gender",
        choices=[
            ('m', 'Male'),
            ('f', 'Female'),
            ('o', 'Other')
        ],
        validators=[DataRequired(message="Gender is required")]
    )
    phone = StringField("Phone number")
    address = StringField("Address")
    city = StringField("City")
    country = StringField("Country")
    password = PasswordField("Password", validators=[DataRequired(), Length(min=4, max=20)])

    submit = SubmitField("Submit")

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=4, max=20)])
    submit = SubmitField("Submit")

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Here we use a class of some kind to represent and validate our
    # client-side form data. For example, WTForms is a library that will
    # handle this for us, and we use a custom LoginForm to validate.
    form = LoginForm()
    if form.validate_on_submit():
        # Login and validate the user.
        # user should be an instance of your `User` class
        # get user from db
        user = User.query.filter_by(email=form.email.data).first()
        login_user(user)
        flash('Logged in successfully.')

        next = request.args.get('next')
  
        return redirect(next or url_for('index'))
    return render_template('login.html', form=form)
@app.route("/custom_login", methods=["GET", "POST"])
def custom_login():
    form = CreateResume()
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                session["user_id"] = user.id
                session["logged_in"] = True
                return redirect(url_for("profile"))
            else:
                return render_template("login.html", error="Wrong password")
        else:
            return render_template("login.html", error="Wrong email")
    return render_template("login.html", form=form)

    return "session started"
    # return render_template("login.html")


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route("/profile")
def profile():
    # flask_login current_user
    if not current_user.is_authenticated:
        return redirect(url_for("login"))
    print(current_user)
    return f"Hello {current_user.name}"


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

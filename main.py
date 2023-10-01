from flask import Flask, render_template, flash, json, redirect, url_for, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from forms import SignUpForm, LoginForm, UploadForm
from flask_login import UserMixin, login_user, logout_user, LoginManager
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask_bootstrap import Bootstrap5
import os

app = Flask(__name__)
app.secret_key = '58o8l.>0d]yj$igr0jtA"6}DI@#JMK'

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(User, user_id)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quotes.db'
db = SQLAlchemy(app)
bootstrap = Bootstrap5(app)


class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    token = db.Column(db.String(100), unique=True, nullable=True)
    quote_packs = relationship("QuotePack", back_populates="owner")


class QuotePack(db.Model):
    __tablename__ = "quote_pack"
    id = db.Column(db.Integer, primary_key=True)
    pack_name = db.Column(db.String(100), unique=True, nullable=False)
    pack_desc = db.Column(db.String(150), unique=True)
    img_path = db.Column(db.String(150), unique=True)
    file_path = db.Column(db.String(150), unique=True)
    owner = relationship("User", back_populates="quote_packs")
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)


with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/Account/SignUp", methods=['GET', 'POST'])
def sign_up():
    form = SignUpForm()
    if form.validate_on_submit():
        if db.session.execute(db.Select(User).where(User.email == form.email.data)).scalar():
            flash("That email address is already in use!")
        else:
            hashed_password = generate_password_hash(form.password.data, salt_length=8)
            new_user = User(email=form.email.data,
                            password=hashed_password)
            db.session.add(new_user)
            db.session.commit()

            login_user(new_user)

            return redirect(url_for("show_collection"))
    return render_template("sign_up.html", form=form)


@app.route("/Account/SignIn", methods=['GET', 'POST'])
def sign_in():
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.execute(db.Select(User).where(User.email == form.email.data)).scalar()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for("collection"))
            else:
                flash("Email or password incorrect.")
        else:
            flash("Email or password incorrect.")
    return render_template("sign_in.html", form=form)


@app.route("/QuotePacks")
def show_collection():
    result = db.session.execute(db.select(QuotePack))
    packs = result.scalars().all()
    return render_template("collection.html", quote_pack=packs)


@app.route("/Upload", methods=['GET', 'POST'])
def upload():
    form = UploadForm()
    if form.validate_on_submit():
        pack_name = secure_filename(form.pack_name.data)

        pack_data = form.pack_file.data
        pack_data_filename = secure_filename(pack_data.filename)
        pack_data_path = f"uploads"

        pack_img = form.pack_image.data
        pack_img_filename = secure_filename(pack_img.filename)
        pack_img_path = f"static/pack_thumbnails"

        pack_data.save(os.path.join(pack_data_path, pack_data_filename))
        pack_img.save(os.path.join(pack_img_path, pack_img_filename))

        with open(f"{pack_data_path}/{pack_data_filename}") as file:
            quotes = json.load(file)
            db.session.add(QuotePack(pack_name=quotes["Name"], pack_desc=quotes["Description"],
                                     file_path=f"{pack_data_path}/{pack_data_filename}",
                                     img_path=f"{pack_img_path}/{pack_img_filename}", owner_id=1))
            db.session.commit()

        return redirect(url_for("show_collection"))

    return render_template("upload.html", form=form)


@app.route('/Download/<path:file_path>', methods=['GET', 'POST'])
def download(file_path):
    return send_from_directory(directory="", path=file_path, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)

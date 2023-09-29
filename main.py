from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quotes.db'
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    token = db.Column(db.String(100), unique=True, nullable=True)
    quote_packs = relationship("QuotePack", back_populates="owner")


class QuotePack(db.Model):
    __tablename__ = "quote_pack"
    id = db.Column(db.Integer, primary_key=True)
    pack_name = db.Column(db.String(100), unique=True, nullable=False)
    pack_desc = db.Column(db.String(150))
    img_url = db.Column(db.String(100))
    file_url = db.Column(db.String(150), unique=True, nullable=False)
    owner = relationship("User", back_populates="quote_packs")
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)


with app.app_context():
    db.create_all()

# with app.app_context():
#     with open("resources/quote_packs/fortunes.txt") as file:
#         quotes = file.read().split("%")
#         for quote in quotes:
#             new_quote = QuotePack


@app.route("/")
def home():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)

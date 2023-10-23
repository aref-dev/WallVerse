from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import SubmitField, PasswordField, EmailField, validators, StringField
from wtforms.validators import DataRequired, Length


class SignUpForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Sign Up")


class LoginForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Sign In")


class UploadForm(FlaskForm):
    pack_name = StringField(validators=[DataRequired(), Length(3, 40)])
    pack_file = FileField("Pack JSON File", validators=[FileRequired()])
    pack_image = FileField("Pack Image File", validators=[FileRequired()])
    submit = SubmitField("Upload Pack")

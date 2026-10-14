from flask_wtf import FlaskForm
from werkzeug.security import generate_password_hash
from wtforms import PasswordField, StringField
from wtforms.validators import DataRequired, Length, EqualTo, Regexp, ValidationError

from extensions import db
from quiz_app.models import User


class LoginForm(FlaskForm):
    username = StringField(
        "Username",
        filters=[lambda v: v.strip() if v else v],
        validators=[DataRequired(), Length(max=255)],
    )
    password = PasswordField("Password", validators=[DataRequired(), Length(max=128)])


class CreateUserForm(FlaskForm):
    username = StringField(
        "Username",
        filters=[lambda v: v.strip() if v else v],
        validators=[
            DataRequired(),
            Length(min=3, max=255),
            Regexp(
                r"^[A-Za-z0-9_.-]+$",
                message="Use only letters, numbers, dots, dashes and underscores.",
            ),
        ],
    )
    password = PasswordField(
        "Password",
        validators=[DataRequired(), Length(min=8, max=128)],
    )
    confirm_password = PasswordField(
        "Repeat password",
        validators=[
            DataRequired(),
            EqualTo("password", message="Passwords must match."),
        ],
    )

    def validate_username(self, field):
        if (
            db.session.scalar(db.select(User).where(User.name == field.data))
            is not None
        ):
            raise ValidationError("That username is already taken.")

    def get_hashed_password(self) -> str:
        return generate_password_hash(self.password.data)

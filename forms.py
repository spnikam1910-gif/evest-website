from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Email, Length, Regexp, Optional

SERVICE_CHOICES = [
    ("", "Select a service"),
    ("strategy-consulting", "Strategy Consulting"),
    ("growth-marketing", "Growth Marketing"),
    ("financial-advisory", "Financial Advisory"),
    ("business-automation", "Business Automation"),
    ("brand-development", "Brand Development"),
    ("other", "Something else"),
]

PHONE_REGEX = r"^[0-9+\-\s()]{7,20}$"


class ContactForm(FlaskForm):
    full_name = StringField(
        "Full Name",
        validators=[DataRequired(message="Please tell us your name."), Length(max=120)],
    )
    email = StringField(
        "Email",
        validators=[DataRequired(message="Please add an email address."), Email(message="That email doesn't look right."), Length(max=255)],
    )
    phone = StringField(
        "Phone Number",
        validators=[
            DataRequired(message="Please add a phone number."),
            Regexp(PHONE_REGEX, message="Please enter a valid phone number."),
        ],
    )
    company_name = StringField("Company Name", validators=[Optional(), Length(max=150)])
    service_interested = SelectField(
        "Service Interested In",
        choices=SERVICE_CHOICES,
        validators=[DataRequired(message="Please select a service.")],
    )
    message = TextAreaField("Message", validators=[Optional(), Length(max=2000)])

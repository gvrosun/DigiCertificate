from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, FileField, SelectField
from wtforms.fields.html5 import EmailField, DateField
from wtforms.validators import DataRequired, EqualTo
from wtforms import ValidationError
from digicert.models import User


class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField()
    submit = SubmitField('Log In')


class RegistrationForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('pass_confirm', message='Passwords Must Match!')])
    pass_confirm = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField('Register!')

    def check_email(self, field):
        # Check if not None for that user email!
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Your email has been registered already!')

    def check_username(self, field):
        # Check if not None for that username!
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Sorry, that username is taken!')


class ForgotPasswordForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    submit = SubmitField('Reset Password')

    def check_email(self, field):
        if User.query.filter_by(email=field.data).first():
            pass
        else:
            raise ValidationError('Your email not registered with us')


class ContactUsForm(FlaskForm):
    name = StringField('Your Name', validators=[DataRequired()])
    email = EmailField('Your Email', validators=[DataRequired()])
    subject = StringField('Subject', validators=[DataRequired()])
    message = TextAreaField('Message', validators=[DataRequired()])
    submit = SubmitField('Submit')


class SubscribeForm(FlaskForm):
    email = EmailField(validators=[DataRequired()])
    submit = SubmitField('Subscribe')


class AddEventForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    logo = FileField('Logo', validators=[DataRequired()])
    mode = SelectField('Category', choices=[('Online', 'Offline'), ('online', 'offline')], validators=[DataRequired()])
    event_date = DateField('Event Date', validators=[DataRequired()])
    submit = SubmitField('Add Event')


class AddCertificateForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    certificate_image = FileField('Certificate', validators=[DataRequired()])
    obtained_date = DateField('Obtained Date', validators=[DataRequired()])
    submit = SubmitField('Add Certificate')

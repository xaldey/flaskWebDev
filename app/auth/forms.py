from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    username = StringField('Username', validators=[
        DataRequired(), Length(1, 64),
        Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
               'Имя пользователя может содержать английские буквыб цифры, точки и подчеркивания.')])
    password = PasswordField('Пароль', validators=[
        DataRequired(), EqualTo('password2', message='Пароли должны совпадать')])
    password2 = PasswordField('Подтверждение пароля', validators=[DataRequired()])
    submit = SubmitField('Зарегистрироваться')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Такой email уже зарегистрирован.')

    def validate_username(self, field):
            if User.query.filter_by(username=field.data).first():
                raise ValidationError('Пользователь с таким именем уже зарегистрирован.')



class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')

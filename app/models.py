from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from . import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Делаю класс Роли для пользователя
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role')

    def __repr__(self):
        return '<Роль %r>' % self.name


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('пароль - не читаемый атрибут')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<Пользователь %r>' % self.username


class NameForm(FlaskForm):
    name = StringField('Как к тебе обращаться?', validators=[DataRequired()])
    submit = SubmitField('Отправить')

#         return f'<Тэг #{self.id} {self.name}>'
#
# class Post(db.Model):
#     __table__ = 'posts'
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
#     title = db.Column(db.String(64), nullable=False)
#     text = db.Column(db.Text, nullable=False)
#     is_published = db.Column(db.Boolean, nullable=False, default=False)
#
#     user = relationship(User, back_populates='posts')
#     tags = relationship('Tag', secondary=posts_tags_table, back_populates='posts')
#
#     def __repr__(self):
#         return f'<Пост #{self.id} от {self.user} {self.title}.'
#
#
# class Tag(db.Model):
#     __tablename__ = 'tags'
#
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(20), nullable=False)
#
#     posts = relationship('Post', secondary=posts_tags_table, back_populates='tags')
#
#     def __repr__(self):


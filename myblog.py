from sqlalchemy.orm import relationship

from config import SECRET_KEY, SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_migrate import Migrate
from flask_login import UserMixin
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config.from_pyfile('config.py')

db = SQLAlchemy(app)
bootstrap = Bootstrap(app)
moment = Moment(app)
migrate = Migrate(app, db)

#
# posts_tags_table = db.Table(
#         'tags_posts',
#         # db.Base.metadata,
#         db.Column('post_id', db.Integer, db.ForeignKey('posts.id'), primary_key=True),
#         db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'), primary_key=True),
#     )

# CREATE TABLE "tags_posts" (
# 	"post_id"	INTEGER,
# 	"tag_id"	INTEGER,
# 	PRIMARY KEY("post_id","tag_id")
# );



# Делаю класс Роли для пользователя
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role')

    def __repr__(self):
        return '<Роль %r>' % self.name


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))


    def __repr__(self):
        return '<Пользователь %r>' % self.username

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
#         return f'<Тэг #{self.id} {self.name}>'


class NameForm(FlaskForm):
    name = StringField('Как к тебе обращаться?', validators=[DataRequired()])
    submit = SubmitField('Отправить')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            db.session.commit()
            session['known'] = False
        else:
            session['known'] = True
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('index'))
    return render_template('index.html',
                           form=form, name=session.get('name'),
                           known=session.get('known', False))

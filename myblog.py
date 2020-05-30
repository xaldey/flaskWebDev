import os
from app import create_app, db
from app.models import User, Role
from flask_migrate import Migrate

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role)


@app.cli.command()
def test():
    """Run the unit tests"""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

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

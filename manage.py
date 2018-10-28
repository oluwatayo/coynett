import os
import unittest
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask import redirect
from app.main.model import models
from app import blueprint

from app.main import create_app, db
from app.main.model.models import Comment

app = create_app(os.getenv('CONFIG_ENV') or 'dev')
app.register_blueprint(blueprint)

app.app_context().push()

manager = Manager(app)

migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)


@manager.command
def run():
    app.run()


@app.route("/")
def hello():
    return redirect('/api/v1/docs')


@manager.command
def test():
    """Runs the unit tests."""
    tests = unittest.TestLoader().discover('app/test', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1

@manager.command
def create_comments():
    for i in range(200):
        comment = Comment(comment='comment'+str(i), post_id=1, user_id=1)
        db.session.add(comment)

    db.session.commit()

    return 1



if __name__ == '__main__':
    manager.run()

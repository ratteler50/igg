import json
import os

from flask import Flask, g, redirect, url_for, render_template
from flask.ext.login import current_user
from flask_admin.contrib.sqla import ModelView

from routes import register_routes
from extensions import login_manager, admin, mail
from ..data.models import Challenge, Game, Interview, MarathonInfo, Prize, ScheduleEntry, User
from ..data.db import db

def create_app(app_config):
    app = Flask(__name__)
    app.config.from_object(app_config)

    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    with open(os.path.join(__location__, 'secrets.json')) as secrets_file:
        secrets = json.load(secrets_file)
        app.secret_key = secrets.get('app_secret')
        app_config.SECRET_KEY = app.secret_key

    login_manager.login_view = 'login.show'

    admin.add_view(AdminModelView(Challenge, db.session))
    admin.add_view(AdminModelView(Game, db.session))
    admin.add_view(AdminModelView(MarathonInfo, db.session))
    admin.add_view(AdminModelView(Prize, db.session))
    admin.add_view(AdminModelView(Interview, db.session))
    admin.add_view(AdminModelView(ScheduleEntry, db.session))

    with open(os.path.join(__location__, 'secrets.json')) as secrets_file:
        secrets = json.load(secrets_file)
        app.config.update(
            MAIL_SERVER='smtp.gmail.com',
            MAIL_PORT=465,
            MAIL_USERNAME='no-reply@iggmarathon.com',
            MAIL_DEFAULT_SENDER='no-reply@iggmarathon.com',
            MAIL_PASSWORD=secrets.get("email_password"),
            MAIL_USE_SSL=True,
            MAIL_USE_TLS=False
        )

    login_manager.init_app(app)
    admin.init_app(app)
    mail.init_app(app)
    register_routes(app)

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.tmpl'), 404

    @login_manager.user_loader
    def load_user(id):
        return db.session.query(User).filter_by(id=id).first()

    @app.context_processor
    def inject_marathon_info():
        marathon_info = getattr(g, "marathon_info", None)
        if not marathon_info:
            marathon_info = g.marathon_info = db.session.query(MarathonInfo).first()
        current_game = db.session.query(Game).filter_by(id=marathon_info.current_game_id).first()
        return dict(marathon_info=marathon_info, current_game=current_game)

    return app

class AdminModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('login', next=request.url))

# IMPORT 여기서 해버리면 한번 미리초기화하는거라서 하면안됨
import config
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from pybo.filter import format_datetime
from sqlalchemy import MetaData
naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

db=SQLAlchemy(metadata=MetaData(naming_convention=naming_convention))

migrate=Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(config)

    # ORM
    db.init_app(app)
    migrate.init_app(app, db)
    if app.config['SQLALCHEMY_DATABASE_URI'].startswith("sqlite"):
        migrate.init_app(app,render_as_batch=True)
    else:
        migrate.init_app(app,db)
    
    
    from . import models
    from.filter import format_datetime
    app.jinja_env.filters['datetime']=format_datetime
    #블루프린트    
    from .views import answer_views, main_views, question_view,auth_views

    # 여기서한번더부르니까 오류생긴것
    app.register_blueprint(main_views.bp)
    app.register_blueprint(question_view.bp)
    app.register_blueprint(answer_views.bp)
    app.register_blueprint(auth_views.bp)
    return app
# flask db init을하려면  set flask_app을 pybo로 기본으로해줘야함 init따라가면안댐



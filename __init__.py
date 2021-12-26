from flask import Flask
from flask_mysqldb import MySQL
from flask_login import login_required,current_user,login_manager,LoginManager


def config():
    app = Flask(__name__)
    app.config['MYSQL_HOST'] = 'host'
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = 'my password'
    app.config['MYSQL_DB'] = 'quizapplicaton'
    app.config['charset'] = "utf-8"
    app.app_context().push()
    mysql = MySQL(app)
    app.secret_key = 'secret key here'

    from profile import profile_blueprint as profile_blueprint
    app.register_blueprint(profile_blueprint)

    from main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    return {'app': app, 'mysql': mysql}

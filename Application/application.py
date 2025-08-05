from Application.views.auth import Auth
from Application.views.contests import Contest
from Application.views.problems import Problems
from Application.views.submission import Submission
from Application.model import db
from flask import Flask
from dotenv import dotenv_values
from flask_swagger_ui import get_swaggerui_blueprint
from flask_migrate import Migrate
from flask_cors import CORS


env = dotenv_values()

def create_app():
    app = Flask(__name__)

    app.register_blueprint(Auth,url_prefix="/auth")
    app.register_blueprint(Contest,url_prefix="/contest")
    app.register_blueprint(Problems,url_prefix="/problems")
    app.register_blueprint(Submission,url_prefix="/submission")

    app.config["SESSION_COOKIE_SAMESITE"] = "None"
    app.config["SESSION_COOKIE_SECURE"] = True
    swaggerui_blueprint = get_swaggerui_blueprint(
        env.get("SWAGGER_URL","/api/docs"),
        "/static/swagger_min.yaml",
        config={ 
            'SERVER_URL': "localhost:5000"
        },
    )
    swaggerui_blueprint_all = get_swaggerui_blueprint(
        "/all"+env.get("SWAGGER_URL","/api/docs/"),
        "/static/swagger.yaml",
        config={ 
            'SERVER_URL': "localhost:5000"
        },
        blueprint_name = "swagger_ui_all"
    )
    app.register_blueprint(swaggerui_blueprint)
    app.register_blueprint(swaggerui_blueprint_all)

    CORS(
        app,
        origins=["*"],
        supports_credentials=True,
        resources={r'/*': {'origins': '*'}},
        methods= "*",
    )

    migrate = Migrate(app, db,  render_as_batch=True)

    app.config["SQLALCHEMY_DATABASE_URI"] = env.get("SQLALCHEMY_DATABASE_URI")
    app.config["SECRET_KEY"] = env.get("SECRET_KEY","SeCrEt KeY")
    db.init_app(app)
    migrate.init_app(app,db)
    app.app_context().push()
    return app



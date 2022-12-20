from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import quote
from flask_login import LoginManager
import cloudinary
from flask_babelex import Babel


app = Flask(__name__)
app.secret_key = '$%^*&())(*&%^%4678675446&#%$%^&&*^$&%&*^&^'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:%s@localhost/qlhs?charset=utf8mb4' % quote('Admin@123')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

cloudinary.config(
  cloud_name = "dyfzuigha",
  api_key = "845545783724776",
  api_secret = "qpXCeoAFOiuT0F_M0sY01YeO91s"
)

login = LoginManager(app=app)

db = SQLAlchemy(app=app)

babel = Babel(app=app)


@babel.localeselector
def load_locale():
    return 'vi'

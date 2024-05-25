import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_uploads import IMAGES, UploadSet, configure_uploads, patch_request_class
from flask_bcrypt import Bcrypt
from werkzeug.utils import secure_filename
import os
from flask_login import LoginManager


basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pedcaneca.db')
app.config['SECRET_KEY'] ='asdf1adf3213'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view='clienteLogin'
login_manager.needs_refresh_message_category='danger'
login_manager.login_message= u"Preencher com os dados de login"

app.config['UPLOADED_PHOTOS_DEST'] = os.path.join(basedir,'static/imagens')
photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)
patch_request_class(app)

from loja.admin import rotas
from loja.produtos import rotas
from loja.carrinho import carrinhos
from loja.clientes import rotas
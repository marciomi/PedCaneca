import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_uploads import IMAGES, UploadSet, configure_uploads, patch_request_class
from flask_bcrypt import Bcrypt
from werkzeug.utils import secure_filename


basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pedcaneca.db')
app.config['SECRET_KEY'] ='asdf1adf3213'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

app.config['UPLOADED_PHOTOS_DEST'] = os.path.join(basedir,'static/imagens')

photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)
patch_request_class(app)


from loja.admin import rotas
from loja.produtos import rotas
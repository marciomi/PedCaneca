from loja import db, app, login_manager
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def user_carregar(user_id):
    return Cadastrar.query.get(user_id)

class Cadastrar(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50), unique = False)
    username = db.Column(db.String(50), unique = True)
    email = db.Column(db.String(50), unique = True)
    password = db.Column(db.String(50), unique = False)    
    state = db.Column(db.String(50), unique = False)
    city = db.Column(db.String(50), unique = False)
    contact = db.Column(db.String(50) ,unique = False)
    address = db.Column(db.String(50) ,unique = False)
    zipcode = db.Column(db.String(50) ,unique = False)
    profile = db.Column(db.String(50), unique = False, default='profile.jpg')
    data_criado = db.Column(db.DateTime, nullable=False,default=datetime.now)
    
    def __repr__(self):
        return '<Cadastrar %r>' % self.name

with app.app_context():
    db.create_all()
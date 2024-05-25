from loja import db, app

from datetime import datetime



class Addproduto(db.Model):    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), nullable=False)
    preco = db.Column(db.Numeric(10,2), nullable=False)
    desconto = db.Column(db.Integer, default=0)
    estoque = db.Column(db.Integer, nullable=False)
    cor = db.Column(db.Text, nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    pub_date = db.Column(db.DateTime, nullable=False, default=datetime.now)

    modelo_id = db.Column(db.Integer, db.ForeignKey('modelo.id'), nullable=False)
    modelo = db.relationship('Modelo', backref=db.backref('modelos', lazy=True))

    tema_id = db.Column(db.Integer, db.ForeignKey('tema.id'), nullable=False)
    tema = db.relationship('Tema', backref=db.backref('temas', lazy=True))

    imagem_1 = db.Column(db.String(150), nullable=False, default='imagem.jpg')
    imagem_2 = db.Column(db.String(150), nullable=False, default='imagem.jpg')
    imagem_3 = db.Column(db.String(150), nullable=False, default='imagem.jpg')

    def __repr__(self):
        return '<Addproduto %r>' % self.nome
    



class Modelo(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(30),nullable=False,unique=True)

class Tema(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(30),nullable=False,unique=True)

#class Cor(db.Model):
#    id = db.Columm(db.Integer,primary_key=True)
#    name = db.Columm(db.String(30),nullable=False,unique=True)

with app.app_context():
    db.create_all()
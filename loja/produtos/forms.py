from flask_wtf.file import FileAllowed, FileField, FileRequired
from wtforms import Form, IntegerField, StringField, BooleanField, TextAreaField, validators, DecimalField


class Addprodutos(Form):
    nome = StringField('Nome :',[validators.DataRequired()])
    preco = DecimalField('Preço :',[validators.DataRequired()])
    desconto = IntegerField('Desconto :',[validators.DataRequired()])
    estoque = IntegerField('Estoque :',[validators.DataRequired()])
    descricao = TextAreaField('Descrição :',[validators.DataRequired()])
    cor = TextAreaField('Cor :',[validators.DataRequired()])
     
    
    imagem_1 = FileField('Imagem 1 :' , validators=[FileRequired(),FileAllowed(['jpg','png','gif','jpeg','bmp'])])
    imagem_2 = FileField('Imagem 2 :' , validators=[FileRequired(),FileAllowed(['jpg','png','gif','jpeg','bmp'])])
    imagem_3 = FileField('Imagem 3 :' , validators=[FileRequired(),FileAllowed(['jpg','png','gif','jpeg','bmp'])])

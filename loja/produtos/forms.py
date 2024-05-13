from flask_wtf.file import FileAllowed, FileField, FileRequired
from wtforms import Form, IntegerField, StringField, BooleanField, TextAreaField, validators, FloatField, SubmitField


class Addprodutos(Form):
    nome = StringField('Nome :',[validators.DataRequired()])
    preco = FloatField('Preço :',[validators.DataRequired()])
    desconto = IntegerField('Desconto :',[validators.DataRequired()])
    estoque = IntegerField('Estoque :',[validators.DataRequired()])
    descricao = StringField('Descrição :',[validators.DataRequired()])
    cor = TextAreaField('Cor :',[validators.DataRequired()])
     
    
    imagem_1 = FileField('Imagem 1 :', validators=[FileAllowed(['jpg','png','gif','jpeg','bmp'])])
    imagem_2 = FileField('Imagem 2 :', validators=[FileAllowed(['jpg','png','gif','jpeg','bmp'])])
    imagem_3 = FileField('Imagem 3 :', validators=[FileAllowed(['jpg','png','gif','jpeg','bmp'])])

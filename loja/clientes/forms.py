from collections.abc import Sequence
from typing import Mapping
from wtforms import Form, SubmitField, IntegerField, FloatField, StringField, TextAreaField, validators, PasswordField, ValidationError
from flask_wtf.file import FileAllowed, FileField, FileRequired
from flask_wtf import FlaskForm
from.model import Cadastrar




class CadastroclienteForm(FlaskForm):
    name = StringField('Nome: ')
    username = StringField('Usuario: ', [validators.DataRequired()])
    email = StringField('Email: ', [validators.DataRequired()])
    password = PasswordField('Senha: ', [validators.DataRequired(), validators.EqualTo('confirm', message='A senha e confirmação de senha tem que ser iguais')])
    confirm = PasswordField('Redigite Senha: ', [validators.DataRequired()])    
    state = StringField('Estado: ', [validators.DataRequired()])
    city = StringField('Cidade: ', [validators.DataRequired()])
    contact = StringField('Telefone: ', [validators.DataRequired()])
    address = StringField('Endereço: ', [validators.DataRequired()])
    zipcode = StringField('CEP: ', [validators.DataRequired()])
    profile = FileField('Perfil', validators=[FileAllowed(['jpg','png','gif','jpeg','bmp'])])
    
    submit = SubmitField('Cadastrar')


    def validate_username(self, username):
        if Cadastrar.query.filter_by(username=username.data).first():
            raise ValidationError("Usuário já existente")
        
    def validate_username(self, email):
        if Cadastrar.query.filter_by(email=email.data).first():
            raise ValidationError("Email já existente")

class ClienteLoginForm(FlaskForm):
    email = StringField('Email: ', [validators.DataRequired()])
    password = PasswordField('Senha: ', [validators.DataRequired()])
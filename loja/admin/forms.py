from wtforms import Form, BooleanField, StringField, PasswordField, validators

class Registrationform(Form):
    name = StringField('Nome completo :', [validators.Length(min=4, max=25)])
    username = StringField('Usuario :', [validators.Length(min=4, max=25)])
    email = StringField('Email :', [validators.Length(min=6, max=35)])
    password = PasswordField('Nova senha', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Senha e confimação de senha não são iguais')
    ])
    confirm = PasswordField('Digite sua senha novamente')

class LoginFormulario(Form):
    email = StringField('Email :', [validators.Length(min=6, max=35)])
    password = PasswordField('Nova senha', [validators.DataRequired()])
    
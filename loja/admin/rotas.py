from flask import render_template, session, request, url_for, flash, redirect
from loja.produtos.models import Addproduto, Modelo, Tema
from loja import app, db, bcrypt
from .forms import LoginFormulario, Registrationform
from .models import User
import os


@app.route('/')
def admin():
    if'email' not in session:
        flash(f'Favor efetuar o login', 'danger')
        return redirect(url_for('login'))
    produtos = Addproduto.query.all()
    return render_template ('admin/index.html', title='Área Administrativa', produtos=produtos)

@app.route('/modelos')
def modelo():
    if'email' not in session:
        flash(f'Favor efetuar o login', 'danger')
        return redirect(url_for('login'))
    modelos = Modelo.query.order_by(Modelo.name).all()
    return render_template ('admin/modelo.html', title='Edição de Modelos', modelos=modelos)

@app.route('/tema')
def tema():
    if'email' not in session:
        flash(f'Favor efetuar o login', 'danger')
        return redirect(url_for('login'))
    temas = Tema.query.order_by(Tema.name).all()
    return render_template ('admin/modelo.html', title='Edição de Temas', temas=temas)

@app.route('/registrar', methods=['GET', 'POST'])
def registrar():
    form = Registrationform(request.form)
    if request.method == 'POST' and form.validate():
        
        hash_password = bcrypt.generate_password_hash(form.password.data)
        user = User(name=form.name.data, username=form.username.data, email=form.email.data,
        password=hash_password)
        db.session.add(user)
        db.session.commit()
        flash(f'{form.name.data} registro criado com sucesso', 'success')

        return redirect(url_for('login'))
    return render_template('admin/registrar.html', form=form, title="Registrar Usuários")

@app.route('/login', methods=['GET', 'POST'])
def login():
    form=LoginFormulario(request.form)
    if request.method =="POST" and form.validate():
        user= User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            session['email'] = form.email.data
            flash(f'Seja bem vindo {form.email.data}', 'success')
            return redirect(request.args.get('next')or url_for('admin'))
        else:
            flash('Email ou senha incorreta')
    return render_template ('admin/login.html', form=form, title='Login')
    


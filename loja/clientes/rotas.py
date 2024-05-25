from flask import render_template, session, request, redirect, url_for, flash, current_app
from flask_bcrypt import Bcrypt
from loja import db, app, photos, bcrypt, login_manager
from .forms import CadastroclienteForm, ClienteLoginForm
import secrets
import os
from.model import Cadastrar
from flask_login import login_required, current_user, login_user, logout_user



@app.route('/cliente/cadastrar', methods=['GET','POST'])
def cadastrar_clientes():
    form = CadastroclienteForm()
    if form.validate_on_submit():
        hash_password = bcrypt.generate_password_hash(form.password.data)
        cadastrar = Cadastrar(name=form.name.data,username=form.username.data,email=form.email.data,password=hash_password,state=form.state.data,city=form.city.data,contact=form.contact.data,address=form.address.data,zipcode=form.zipcode.data,profile=form.profile.data)
        db.session.add(cadastrar)
        flash(f'{form.name.data} - Seu usuário foi cadastrado com sucesso', 'success')
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('cliente/cliente.html', form=form)

@app.route('/cliente/login', methods=['GET','POST'])
def clienteLogin():
    form = ClienteLoginForm()
    if form.validate_on_submit():
        user = Cadastrar.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Usuário logado', 'success')
            next = request.args.get('next')
            return redirect(next or url_for('home'))
        flash('Senha ou email incorreto', 'danger')
        return redirect(url_for('clienteLogin'))
    return render_template('cliente/login.html', form=form)




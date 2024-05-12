from flask import redirect, render_template, url_for, flash, request, session
from .forms import Addprodutos
from loja import db, app, photos
from .models import Modelo, Tema, Addproduto
import secrets

@app.route('/addmodelo', methods=['GET','POST'])
def addmodelo():
    if'email' not in session:
        flash(f'Favor efetuar o login', 'danger')
        return redirect(url_for('login'))
    
    if request.method=="POST":
        getmodelo = request.form.get('modelo')
        modelo = Modelo(name=getmodelo)
        db.session.add(modelo)
        flash(f'O modelo {getmodelo} cadastrada com sucesso', 'success')
        db.session.commit()
        return redirect(url_for('addmodelo'))
    return render_template('/produtos/addmodelo.html', modelo='modelo')

@app.route('/addtema', methods=['GET','POST'])
def addtema():
    if'email' not in session:
        flash(f'Favor efetuar o login', 'danger')
        return redirect(url_for('login'))
    
    if request.method=="POST":
        getmodelo = request.form.get('tema')
        tema = Tema(name=getmodelo)
        db.session.add(tema)
        flash(f'O Tema {getmodelo} cadastrada com sucesso', 'success')
        db.session.commit()
        return redirect(url_for('addtema'))
    return render_template('/produtos/addmodelo.html')

@app.route('/addproduto', methods=['GET','POST'])
def addproduto():
    if'email' not in session:
        flash(f'Favor efetuar o login', 'danger')
        return redirect(url_for('login'))
    modelos = Modelo.query.all()
    temas = Tema.query.all()
    form = Addprodutos(request.form)
    if request.method=="POST":
        nome = form.nome.data
        preco = form.preco.data
        desconto = form.desconto.data
        estoque = form.estoque.data
        cor = form.cor.data
        descricao = form.descricao.data
        modelo = request.form.get('modelo')
        tema = request.form.get('tema')
        imagem_1 = photos.save(request.files.get('imagem_1'),name=secrets.token_hex(10)+".")
        imagem_2 = photos.save(request.files.get('imagem_2'),name=secrets.token_hex(10)+".")
        imagem_3 = photos.save(request.files.get('imagem_3'),name=secrets.token_hex(10)+".")

        addpro = Addproduto(nome=nome, preco=preco, desconto=desconto, estoque=estoque, cor=cor, descricao=descricao, modelo_id=modelo, tema_id=tema, imagem_1=imagem_1, imagem_2=imagem_2, imagem_3=imagem_3)
        db.session.add(addpro)
        flash(f'Produto {nome} foi cadastrado com sucesso', 'success')
        db.session.commit()
        return redirect(url_for('admin')) 
    return render_template('produtos/addproduto.html', title="Cadastrar Produtos",form=form, modelos=modelos, temas=temas)

@app.route('/atualizarmodelo/<int:id>', methods=['GET','POST'])
def atualizarmodelo(id):
    if'email' not in session:
        flash(f'Favor efetuar o login', 'danger')
        return redirect(url_for('login'))
    atualizarmodelo = Modelo.query.get_or_404(id)
    modelo = request.form.get('modelo')
    if request.method=='POST':
        atualizarmodelo.name = modelo
        flash(f'O modelo foi atualizado com sucesso', 'success')
        db.session.commit()
        return redirect(url_for('modelo'))
    return render_template('/produtos/atualizarmodelo.html', title='Atualizar Modelos', atualizarmodelo=atualizarmodelo)

@app.route('/atualizartema/<int:id>', methods=['GET','POST'])
def atualizartema(id):
    if'email' not in session:
        flash(f'Favor efetuar o login', 'danger')
        return redirect(url_for('login'))
    atualizartema = Tema.query.get_or_404(id)
    tema = request.form.get('tema')
    if request.method=='POST':
        atualizartema.name = tema
        flash(f'O tema foi atualizado com sucesso', 'success')
        db.session.commit()
        return redirect(url_for('tema'))
    return render_template('/produtos/atualizarmodelo.html', title='Atualizar Temas', atualizartema=atualizartema)

@app.route('/atualizarproduto/<int:id>', methods=['GET','POST'])
def atualizarproduto(id):
    modelos = Modelo.query.all()
    temas = Tema.query.all()
    produto = Addproduto.query.get_or_404(id)
    modelo = request.form.get('modelo')
    tema = request.form.get('tema')
    form = Addprodutos(request.form)
    if request.method== "POST":
        produto.nome = form.nome.data
        produto.preco = form.preco.data
        produto.desconto = form.desconto.data
        produto.estoque = form.estoque.data
        produto.modelo_id = modelo
        produto.tema_id = tema
        produto.cor = form.cor.data
        produto.descricao = form.descricao.data

        db.session.commit()
        flash(f'O produto foi atualizado com sucesso', 'success')
        return redirect('/')

    form.nome.data = produto.nome
    form.preco.data = produto.preco
    form.desconto.data = produto.desconto
    form.estoque.data = produto.estoque
    form.cor.data = produto.cor
    form.descricao.data = produto.descricao
   
    

    return render_template('/produtos/atualizarproduto.html', title='Atualizar Produtos', form=form, modelos=modelos, temas=temas, produto=produto, modelo=modelo, tema=tema)
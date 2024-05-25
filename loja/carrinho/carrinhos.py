from flask import redirect, render_template, url_for, flash, request, session, current_app
from loja import db, app
from loja.produtos.models import Addproduto
from loja.produtos.rotas import modelos, temas
import json



def M_Dicionarios(dic1,dic2):
    if isinstance(dic1,list) and isinstance(dic2,list):
        return dic1 + dic2
    elif isinstance(dic1,dict) and isinstance(dic2,dict):
        return dict(list(dic1.items()) + list(dic2.items()))
    return False

@app.route('/addCart', methods=['POST'])
def AddCart():
    try:
        produto_id = request.form.get('produto_id')
        quantidade = int(request.form.get('quantidade'))
        cor = request.form.get('cor')
        produto = Addproduto.query.filter_by(id=produto_id).first()

        if produto_id and quantidade and cor and request.method =="POST":
            DicItems = {produto_id:{'nome':produto.nome, 'preco':float(produto.preco), 'desconto':produto.desconto, 'cor':produto.cor, 'quantidade':produto.estoque, 'imagem':produto.imagem_1, 'cores':cor}}
            if 'LojainCarrinho' in session:
                print(session['LojainCarrinho'])
                if produto_id in session['LojainCarrinho']:
                    if produto_id in session['LojainCarrinho']:
                        for key, item in session['LojainCarrinho'].items():
                            if int(key) ==int(produto_id):
                                session.modified = True
                                item['quantidade']+=1
                else:
                    session['LojainCarrinho'] = M_Dicionarios(session['LojainCarrinho'],DicItems)
                    return redirect(request.referrer)
                
            else:
                session['LojainCarrinho'] = DicItems
                return redirect(request.referrer)

    except Exception as e:
        print(e)
    finally:
        return redirect(request.referrer)

@app.route('/carros')
def getCart():
    if 'LojainCarrinho' not in session or len(session['LojainCarrinho']) <=0:
        return redirect(url_for('home'))
    subtotal = 0
    valorpagar = 0
    for key, produto in session['LojainCarrinho'].items():
        desconto = (produto['desconto']/100) * float(produto['preco'])
        subtotal += float(produto['preco']) * int(produto['quantidade'])
        subtotal -= desconto
        imposto = ("%.2f"% (.06 * float(subtotal)))
        valorpagar = float("%.2f" %(1.06 * subtotal))
    return render_template('produtos/carros.html', imposto=imposto, valorpagar=valorpagar, modelos=modelos(), temas=temas())


@app.route('/updateCarro/<int:code>', methods=['POST'])
def updateCarro(code):
    if 'LojainCarrinho' not in session or len(session['LojainCarrinho']) <=0:
        return redirect(url_for('home'))
    if request.method == "POST":
        quantidade = request.form.get('quantidade')
        cores = request.form.get('cores')
        try:
            session.modified = True
            for key, item in session['LojainCarrinho'].items():
                if int(key) == code:
                    item['quantidade']= quantidade
                    item['cores']= cores
                    flash('Item atualizado com sucesso')
                    return redirect(url_for('GetCart'))                
        except Exception as e:
            print(e)
            return redirect(url_for('getCart'))
        

@app.route('/deleteitem/<int:id>')
def deleteitem(id):
    if 'LojainCarrinho' not in session or len(session['LojainCarrinho'])<=0:
        return redirect(url_for('home')) 
    try:
        session.modified = True
        for key, item in session['LojainCarrinho'].items():
            if int(key) == id:
                session['LojainCarrinho'].pop(key,None)       
                flash('Item atualizado com sucesso')
                return redirect(url_for('GetCart'))                
    except Exception as e:
        print(e)
        return redirect(url_for('getCart'))
    
@app.route('/limparcarro')
def limparcarro():
    try:
        session.pop('LojainCarrinho',None)
        return redirect(url_for('home'))                
    except Exception as e:
        print(e)
        

from flask import render_template, session, request, redirect, url_for, flash, current_app, make_response, Flask, jsonify
from flask_bcrypt import Bcrypt
from loja import db, app, photos, bcrypt, login_manager
from .forms import CadastroclienteForm, ClienteLoginForm
import secrets
import os
from .model import Cadastrar, ClientePedido
from flask_login import login_required, current_user, login_user, logout_user
import pdfkit
import base64
import stripe


publishable_key = 'pk_test_51QLvO3C6EyAXa8556fixSAOiCkDVAjI6xP7bqgvqDJ4b5BRuV4Z0IWyKYM44x1miqrBu8Hb2GmEHo4sLga0yJY7W00pnnBpGHJ'
stripe.api_key = 'sk_test_51QLvO3C6EyAXa855SjPCA9XD6Fgy7bZbSRoFo6JlFDDMmdJolEN5PKyPtIXxTbhzZTOaH4oUF9Pgv3U0hCoox1CR004oN7lFxX'

@app.route('/pagamento', methods=['POST'])
@login_required
def pagamento():
    notafiscal = request.form.get('invoice')
    amount = request.form.get('amount')
    
    customer = stripe.Customer.create(
        email=request.form['stripeEmail'],
        source=request.form['stripeToken'],
    )

    charge = stripe.Charge.create(
        customer=customer.id,
        description='PedCaneca',
        amount=int(amount),
        currency='brl',
    )
    cliente_pedido = ClientePedido.query.filter_by(cliente_id=current_user.id, notafiscal=notafiscal).order_by(ClientePedido.id.desc()).first()
    cliente_pedido.status='pago'
    db.session.commit()
    return redirect(url_for('obrigado'))
   
@app.route('/obrigado')
def obrigado():
    return render_template('cliente/obrigado.html')


@app.route('/cliente/cadastrar', methods=['GET','POST'])
def cadastrar_clientes():
    form = CadastroclienteForm()
    if form.validate_on_submit():
        hash_password = bcrypt.generate_password_hash(form.password.data)
        cadastrar = Cadastrar(name=form.name.data,username=form.username.data,email=form.email.data,password=hash_password,state=form.state.data,city=form.city.data,contact=form.contact.data,address=form.address.data,zipcode=form.zipcode.data,profile=form.profile.data)
        db.session.add(cadastrar)
        flash(f'{form.name.data} - Seu usuário foi cadastrado com sucesso', 'success')
        db.session.commit()
        return redirect(url_for('clienteLogin'))
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

@app.route('/cliente/logout')
def cliente_logout():
    logout_user()
    return redirect(url_for('home'))

def atualizarlojaCarro():
    for _key, produto in session['LojainCarrinho'].items():
        session.modified = True
        del produto['imagem']
        del produto['cor']

    return atualizarlojaCarro


@app.route('/pedido_order')
@login_required
def pedido_order():
    if current_user.is_authenticated:
        cliente_id = current_user.id
        notafiscal = secrets.token_hex(5)
        atualizarlojaCarro()

        try:
            p_order = ClientePedido(notafiscal=notafiscal, cliente_id=cliente_id, pedido=session['LojainCarrinho'])
            db.session.add(p_order)
            db.session.commit()
            session.pop('LojainCarrinho')
            flash('Pedido criado com sucesso', 'success')
            return redirect(url_for('pedidos',notafiscal=notafiscal))
        except Exception as e:
            print(e)
            flash('Não foi possível processar seu pedido', 'danger')
            return redirect(url_for('getCart'))

@app.route('/pedidos/<notafiscal>')
@login_required
def pedidos(notafiscal):
    if current_user.is_authenticated:
        gTotal = 0
        subTotal = 0
        cliente_id = current_user.id
        cliente = Cadastrar.query.filter_by(id=cliente_id).first()
        pedidos = ClientePedido.query.filter_by(cliente_id=cliente_id, notafiscal=notafiscal).order_by(ClientePedido.id.desc()).first()
        for _key, produto in pedidos.pedido.items():
            desconto = (produto['desconto']/100) * float(produto['preco'])
            subTotal += float(produto['preco']) * int(produto['quantidade'])
            subTotal -= desconto
            imposto =("%.2f" % (.06 * float(subTotal)))
#            gTotal = float("%.2f" % (1.06 * subTotal))
            gTotal = subTotal
    else:
        return redirect(url_for('clienteLogin'))
    return render_template('cliente/pedido.html', notafiscal=notafiscal, imposto=imposto, subTotal=subTotal,  gTotal=gTotal, cliente=cliente, pedidos=pedidos)

@app.route('/get_pdf/<notafiscal>', methods=['POST'])
@login_required
def get_pdf(notafiscal):
    if current_user.is_authenticated:
        gTotal = 0
        subTotal = 0
        cliente_id = current_user.id
        if request.method == "POST":            
            cliente = Cadastrar.query.filter_by(id=cliente_id).first()
            pedidos = ClientePedido.query.filter_by(cliente_id=cliente_id, notafiscal=notafiscal).order_by(ClientePedido.id.desc()).first()
            for _key, produto in pedidos.pedido.items():
                desconto = (produto['desconto']/100) * float(produto['preco'])
                subTotal += float(produto['preco']) * int(produto['quantidade'])
                subTotal -= desconto
                imposto =("%.2f" % (.06 * float(subTotal)))
#                gTotal = float("%.2f" % (1.06 * subTotal))
                gTotal = subTotal           
            image_path = os.path.join(current_app.root_path, 'static/imagens/icone_caneca_Pedcaneca.png')            
            with open(image_path, 'rb') as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
                base64_string = f"data:image/png;base64,{encoded_string}"

            path_wkhtmltopdf = 'loja/wkhtmltopdf.exe'
            config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
            options = {
                'enable-local-file-access': None,
            }
            rendered = render_template('cliente/pdf.html', notafiscal=notafiscal, imposto=imposto, subTotal=subTotal, gTotal=gTotal, cliente=cliente, pedidos=pedidos, base64_string=base64_string)
            pdf = pdfkit.from_string(rendered, False, configuration=config, options=options)
            response = make_response(pdf)
            response.headers['Content-Type'] = 'application/pdf'
            response.headers['Content-Disposition'] = 'inline; filename=' + notafiscal + '.pdf'
            return response
    return redirect(url_for('pedidos'))

@app.route('/meus_pedidos/<int:cliente_id>')
def pedidos_cliente(cliente_id):
    cliente = Cadastrar.query.get_or_404(cliente_id)
    pedidos = ClientePedido.query.filter_by(cliente_id=cliente_id).order_by(ClientePedido.data_criado.desc()).all()

    for pedido in pedidos:
        valor_total = 0
        for key, produto in pedido.pedido.items():
            quantidade = float(produto.get('quantidade', 0))
            preco = float(produto.get('preco', 0))
            desconto = (produto.get('desconto', 0) / 100) * preco
            subtotal = quantidade * preco
            subtotal_com_desconto = subtotal - desconto
            valor_total += subtotal_com_desconto
        pedido.valor_total = valor_total

    return render_template('cliente/meus_pedidos.html', cliente=cliente, pedidos=pedidos)

@app.route('/meus_pedidos/')
def listar_pedidos():
    clientes_com_pedidos = []

    # Obtenha todos os clientes
    clientes = Cadastrar.query.all()
    for cliente in clientes:
        # Obtenha os pedidos do cliente e ordene por data de criação, mais recente primeiro
        pedidos = ClientePedido.query.filter_by(cliente_id=cliente.id).order_by(ClientePedido.data_criado.desc()).all()
        
        if pedidos:  # Verifique se o cliente tem pedidos
            for pedido in pedidos:
                valor_total = 0
                for key, produto in pedido.pedido.items():
                    quantidade = float(produto.get('quantidade', 0))
                    preco = float(produto.get('preco', 0))
                    desconto = (produto.get('desconto', 0) / 100) * preco
                    subtotal = quantidade * preco
                    subtotal_com_desconto = subtotal - desconto
                    valor_total += subtotal_com_desconto
                pedido.valor_total = valor_total
            
            clientes_com_pedidos.append({
                'cliente': cliente,
                'pedidos': pedidos
            })

    # Ordene os clientes por data do pedido mais recente para o mais antigo
    clientes_com_pedidos.sort(key=lambda x: x['pedidos'][0].data_criado, reverse=True)

    return render_template('cliente/meus_pedidos.html', pedidos_por_cliente=clientes_com_pedidos)



@app.route('/atualizar_status', methods=['POST'])
def atualizar_status():
    data = request.get_json()
    notafiscal = data.get('notafiscal')
    status = data.get('status')

    pedido = ClientePedido.query.filter_by(notafiscal=notafiscal).first()
    if pedido:
        pedido.status = status
        db.session.commit()
        return jsonify(success=True)
    return jsonify(success=False)



#PAGINAS DE ACESSIBILIDADE

@app.route('/cliente/cadastrar1', methods=['GET','POST'])
def cadastrar_clientes1():
    form = CadastroclienteForm()
    if form.validate_on_submit():
        hash_password = bcrypt.generate_password_hash(form.password.data)
        cadastrar = Cadastrar(name=form.name.data,username=form.username.data,email=form.email.data,password=hash_password,state=form.state.data,city=form.city.data,contact=form.contact.data,address=form.address.data,zipcode=form.zipcode.data,profile=form.profile.data)
        db.session.add(cadastrar)
        flash(f'{form.name.data} - Seu usuário foi cadastrado com sucesso', 'success')
        db.session.commit()
        return redirect(url_for('clienteLogin1'))
    return render_template('cliente/cliente1.html', form=form)

@app.route('/cliente/login1', methods=['GET','POST'])
def clienteLogin1():
    form = ClienteLoginForm()
    if form.validate_on_submit():
        user = Cadastrar.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Usuário logado', 'success')
            next = request.args.get('next')
            return redirect(next or url_for('home1'))
        flash('Senha ou email incorreto', 'danger')
        return redirect(url_for('clienteLogin1'))
    return render_template('cliente/login1.html', form=form)

@app.route('/cliente/logout1')
def cliente_logout1():
    logout_user()
    return redirect(url_for('home1'))

@app.route('/pedido_order1')
@login_required
def pedido_order1():
    if current_user.is_authenticated:
        cliente_id = current_user.id
        notafiscal = secrets.token_hex(5)
        try:
            p_order = ClientePedido(notafiscal=notafiscal, cliente_id=cliente_id, pedido=session['LojainCarrinho'])
            db.session.add(p_order)
            db.session.commit()
            session.pop('LojainCarrinho')
            flash('Pedido criado com sucesso', 'success')
            return redirect(url_for('pedidos',notafiscal=notafiscal))
        except Exception as e:
            print(e)
            flash('Não foi possível processar seu pedido', 'danger')
            return redirect(url_for('getCart1'))


from flask import Flask, render_template, request, redirect, session, flash, url_for

app = Flask(__name__)
app.secret_key = 'partyou'

class Item():
    def __init__(self, nome, preco):
        self.nome = nome
        self.preco = preco

class Usuario:
    def __init__(self, id, nome, senha):
        self.id = id
        self.nome = nome
        self.senha = senha

usuario1 = Usuario('nana', 'Adriana Garcia', '1234')
usuario2 = Usuario('line', 'Aline Garcia', '4321')
usuario3 = Usuario('fefe', 'Fernanda Souza', '5678')

usuarios = { usuario1.id: usuario1, usuario2.id: usuario2, usuario3.id: usuario3 }

item1 = Item('batata', '2.99')
item2 = Item('arroz', '4.89')
item3 = Item('feijao', '5.60')
lista = [item1, item2, item3]

@app.route('/')
def index():
    return render_template('lista.html', titulo='Itens Disponíveis', itens=lista)

@app.route('/novo')
def novo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('novo')))
    return render_template('adicionar.html', titulo="Novo item")

@app.route('/criar', methods=['POST',])
def criar():
    nome = request.form['nome']
    preco = request.form['preco']
    item = Item(nome, preco)
    lista.append(item)
    return redirect(url_for('index'))

@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima=proxima)

@app.route('/autenticar', methods=['POST'])
def autenticar():
    if request.form['usuario'] in usuarios:
        usuario = usuarios[request.form['usuario']]
        if usuario.senha == request.form['senha']:
            session['usuario_logado'] = usuario.id
            flash(usuario.nome + ' logou com sucesso!')
            proxima_pagina = request.form['proxima']
            return redirect(proxima_pagina)
    else :
        flash('Não logado, tente de novo!')
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Nenhum usuário logado!')
    return redirect(url_for('index'))

app.run(debug=True)

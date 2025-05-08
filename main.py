from flask import Flask, request, redirect, render_template, flash
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = 'chavemuitosecretacomçparahackeramericanonaoconseguirinvadir'

livros = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/catalogo')
def catalogo():
    return render_template('catalogo.html', livros=livros)

@app.route('/adicionar_livro', methods=['GET', 'POST'])
def adicionar_livro():
    if request.method == 'POST':
        nome = request.form['nome']
        autor = request.form['autor']
        ano = request.form['ano']
        codigo = len(livros)
        livros.append([codigo, nome, autor, ano])
        flash('Livro cadastrado com sucesso!')
        return redirect('/catalogo')
    else:
        return render_template('adicionar_livro.html')

@app.route('/editar_livro/<int:codigo>', methods=['GET', 'POST'])
def editar_livro(codigo):
    if request.method == 'POST':
        nome = request.form['nome']
        autor = request.form['autor']
        ano = request.form['ano']
        livros[codigo] = [nome, autor, ano]
        flash('Livro editado com sucesso!')
        return redirect('/catalogo')
    else:
        livro = livros[codigo]
        return render_template('editar_livro.html', livro=livro)

@app.route('/apagar_livro/<int:codigo>')
def apagar_livro(codigo):
    del livros[codigo]
    flash('Livro apagado com sucesso! :(')
    return redirect('/catalogo')

@app.route('/emprestar_livro/<int:codigo>')
def emprestar_livro(codigo):
    hoje = datetime.now()
    devolver = (hoje + timedelta(days = +7)).strftime("%d/%m/%y")
    livros[codigo].append(devolver)
    return redirect('/catalogo')


if __name__ == '__main__':
    app.run(debug=True)
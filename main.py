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
        livros.append({
            'nome': request.form['nome'],
            'autor': request.form['autor'],
            'ano': request.form['ano'],
            'devolver_ate': "",
            'emprestado': False
        })
        flash('Livro cadastrado com sucesso!')
        return redirect('/catalogo')
    else:
        return render_template('adicionar_livro.html')

@app.route('/editar_livro/<int:indice>', methods=['GET', 'POST'])
def editar_livro(indice):

    if request.method == 'POST':
        livros[indice]['nome'] = request.form['nome']
        livros[indice]['autor'] = request.form['autor']
        livros[indice]['ano'] = request.form['ano']
        flash('Livro editado com sucesso!')
        return redirect('/catalogo')
    else:
        livro = livros[indice]
        return render_template('editar_livro.html', livro=livro)

@app.route('/apagar_livro/<int:indice>')
def apagar_livro(indice):
    del livros[indice]
    flash('Livro apagado com sucesso! :(')
    return redirect('/catalogo')

@app.route('/emprestar_livro/<int:indice>')
def emprestar_livro(indice):
    if livros[indice]['emprestado'] == False:
        hoje = datetime.now()
        devolver = (hoje + timedelta(days = -7)).strftime("%d/%m/%y")
        livros[indice]['devolver_ate'] = devolver
    livros[indice]['emprestado'] = True
    flash("Livro emprestado com sucesso!!")
    return redirect('/catalogo')

@app.route('/devolver_livro/<int:indice>')
def devolver_livro(indice):
    hoje = datetime.now()
    devolver = (hoje + timedelta(days=-7)).strftime("%d")
    if livros[indice]['emprestado']:
        livros[indice]['emprestado'] = False
        livros[indice]['devolver_ate'] = ''
    multa = 10+(10*1/100*int(devolver))
    flash(multa)
    return redirect('/catalogo')

if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, jsonify, request, render_template, redirect, url_for, flash
import dados

biblioteca = dados.data_prep()

app = Flask(__name__)
app.config['SECRET_KEY'] = "Wr3nLyr@1275"

@app.route('/')
def check():
    return "O servidor esta no ar"

@app.route('/jogos')
def abrir_bibilioteca():
    biblioteca = dados.data_prep()
    return render_template('biblioteca.html', biblioteca = biblioteca)

@app.route('/jogos/criar', methods=['GET', 'POST'])
def criar_jogo():
    if request.method == 'POST':
        codigo_ult = len(biblioteca) + 1
        new_game = {
            'código': str(codigo_ult),
            'nome': request.form.get('nome'),
            'gênero': request.form.get('genero'),
            'preço': request.form.get('preco')}
        for j in biblioteca:
            if j['código'] == new_game['código']:
                return jsonify("Erro: Jogo ja existe"), 200
        biblioteca.append(new_game)
        dados.save(biblioteca)
        return redirect(url_for('abrir_bibilioteca')), 201
    else:
        return render_template('create.html'), 200

@app.route('/jogos/update', methods=['POST'])
def atualizar_jogo():
    if request.method == 'POST' and request.form.get('type') == 'update':
        updated_game = {
            'código': request.form.get('codigo'),
            'nome': request.form.get('nome'),
            'gênero': request.form.get('genero'),
            'preço': request.form.get('preco')}
        for j in biblioteca:
            if j['código'] == updated_game['código']:
                for key, values in updated_game.items():
                        j[key] = values
                dados.save(biblioteca)
                return redirect(url_for('abrir_bibilioteca')), 200
        return "Errou otário!"

    else:
        codigo = request.form.get('codigo')
        nome = request.form.get('nome')
        genero = request.form.get('genero')
        preco = request.form.get('preco')
        return render_template('update.html', codigo=codigo, nome=nome, genero=genero, preco=preco), 200
        
@app.route('/jogos/delete/<codigo>', methods=['POST'])
def deletar_jogo(codigo):
    biblioteca = dados.data_prep()

    for jogo in biblioteca:
        if jogo['código'] == str(codigo):
            nome = jogo['nome']
            break
    biblioteca = dados.data_prep()
    biblioteca = [livro for livro in biblioteca if livro['código'] != codigo]
    dados.save(biblioteca)
    flash(f'O jogo: {nome} foi deletado com sucesso!', 'success')
    return redirect(url_for('abrir_bibilioteca')), 200



if __name__ == "__main__":
    app.run(debug = True)
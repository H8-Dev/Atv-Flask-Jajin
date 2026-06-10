from flask import Flask, jsonify, request, render_template
import dados

biblioteca = dados.data_prep()

app = Flask(__name__)

@app.route('/')
def check():
    return print("O servidor esta no ar")

@app.route('/biblioteca', methods=['GET', 'POST'])
@app.route('/biblioteca/<codigo>', methods=['GET', 'DELETE', 'PUT'])
def manipula_biblioteca(codigo = None):
    metodo = request.method
    match metodo:
        case 'GET':
            if codigo:
                for j in biblioteca:
                    if j['código'] == codigo:
                        return jsonify(j)
                return jsonify("Error: Jogo não existe na biblioteca"), 404
            else: 
                return jsonify(biblioteca), 200

        case 'POST':
            novo_jogo = request.get_json()
            for j in biblioteca:
                if j['código'] == novo_jogo['código']:
                    return jsonify("Erro: Jogo já existe"), 200
            biblioteca.append(novo_jogo)
            dados.save(biblioteca)
            return jsonify("Jogo cadastrado com sucesso."), 201

        case 'DELETE':
            for j in biblioteca:
                if j['código'] == codigo:
                    biblioteca.remove(j)
            return jsonify("Jogo deletado com sucesso.")
        
        case 'PUT':
            update = request.get_json()
            for j in biblioteca:
                if j['código'] == update['código']:
                    for key, values in update.items():
                        j[key] = values
                    dados.save(biblioteca)
                    return jsonify("Jogo atualizado com sucesso"), 201
            return jsonify("Error: Jogo não existe na biblioteca"), 404

@app.route('/jogos')
def abrir_bibilioteca():
    return render_template('biblioteca.html', biblioteca = biblioteca)

@app.route('/jogos/criar', methods=['GET', 'POST'])
def criar_jogo():
    if request.method == 'POST':
        new_game = {
            'código': request.form.get('codigo'),
            'nome': request.form.get('nome'),
            'gênero': request.form.get('genero'),
            'preço': request.form.get('preco'),
            }
        for j in biblioteca:
            if j['código'] == new_game['código']:
                return jsonify("Erro: Jogo já existe"), 200
        
        biblioteca.append(new_game)
        dados.save(biblioteca)
        return render_template('biblioteca.html', biblioteca = biblioteca)
    else:
        return render_template('criar_jogo.html')




if __name__ == "__main__":
    app.run(debug = True)
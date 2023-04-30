import mysql.connector
from flask import Flask, jsonify, request
from variables import dbpassword

app = Flask(__name__)

conn = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password=f"{dbpassword}",
    database="impacta"
)

print('Conectando ao banco...')

@app.route('/', methods=['GET'])
def index():
    return "Olá, você pode acessar as seguintes URI: /players para verificar todos os jogadores da Impacta \nPara inserir novos jogadores insira conforme o manual do READme.md, caso não tenha acesso a este arquivo, registre novos jogadores na seguinte URI: (/players/insert/<nome>/<categoria>/<console>)\nPara excluir um jogador basta acessar esta URI /players/delete/<id>"

@app.route('/players', methods=['GET'])
def obter_players():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM players")
    result = cursor.fetchall()
    cursor.close()
    return jsonify(result)

# Rota POST que insere um novo registro na tabela "players"
@app.route('/players/insert/<string:nome>/<string:categoria>/<string:console>', methods=['POST'])
def adicionar_pessoa(nome, categoria, console):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO players (nome, categoria, console) VALUES (%s, %s, %s)", (nome, categoria, console))
    conn.commit()
    cursor.close()
    return "Registro adicionado com sucesso!"

@app.route('/players/delete/<int:id>', methods=['DELETE'])
def remover_pessoa(id):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM players WHERE id=%s", (id,))
    conn.commit()
    cursor.close()
    return "Registro removido com sucesso!"

if __name__ == '__main__':
    app.run(port=5004, debug=True)
Footer
© 2023 GitHub, Inc.
Footer navigation
Terms
Privacy

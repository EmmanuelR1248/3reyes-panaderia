from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

DATA_FILE = 'pedidos.json'

def read_pedidos():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def write_pedidos(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

@app.route('/api/pedidos', methods=['GET'])
def get_pedidos():
    return jsonify(read_pedidos())

@app.route('/api/pedidos', methods=['POST'])
def add_pedido():
    pedidos = read_pedidos()
    nuevo_pedido = request.json
    pedidos.append(nuevo_pedido)
    write_pedidos(pedidos)
    return jsonify({'status': 'success'}), 201

@app.route('/api/pedidos/<int:pedido_id>', methods=['PUT'])
def update_pedido(pedido_id):
    pedidos = read_pedidos()
    nuevo_estado = request.json.get('estado')
    for pedido in pedidos:
        if pedido['id'] == pedido_id:
            pedido['estado'] = nuevo_estado
            break
    write_pedidos(pedidos)
    return jsonify({'status': 'success'})

@app.route('/api/pedidos/<int:pedido_id>', methods=['DELETE'])
def delete_pedido(pedido_id):
    pedidos = read_pedidos()
    pedidos = [p for p in pedidos if p['id'] != pedido_id]
    write_pedidos(pedidos)
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
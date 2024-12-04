from flask import Flask, jsonify, request, render_template
import json
import os

app = Flask(__name__)

DATA_FILE = 'videogames.json'

def read_data():
    with open(DATA_FILE, 'r') as file:
        return json.load(file)

def write_data(data):
    with open(DATA_FILE, 'w') as file:
        json.dump(data, file, indent=2)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/videogames', methods=['GET'])
def get_videogames():
    videogames = read_data()
    return jsonify(videogames)

@app.route('/videogames/<int:id>', methods=['GET'])
def get_videogame(id):
    videogames = read_data()
    videogame = next((vg for vg in videogames if vg['id'] == id), None)
    if videogame:
        return jsonify(videogame)
    return jsonify({'message': 'Videogame not found'}), 404

@app.route('/videogames', methods=['POST'])
def create_videogame():
    new_videogame = request.json
    videogames = read_data()
    new_videogame['id'] = videogames[-1]['id'] + 1 if videogames else 1
    videogames.append(new_videogame)
    write_data(videogames)
    return jsonify(new_videogame), 201

@app.route('/videogames/<int:id>', methods=['PUT'])
def update_videogame(id):
    videogames = read_data()
    for i, vg in enumerate(videogames):
        if vg['id'] == id:
            videogames[i] = {**vg, **request.json}
            write_data(videogames)
            return jsonify(videogames[i])
    return jsonify({'message': 'Videogame not found'}), 404

@app.route('/videogames/<int:id>', methods=['DELETE'])
def delete_videogame(id):
    videogames = read_data()
    new_videogames = [vg for vg in videogames if vg['id'] != id]
    if len(new_videogames) != len(videogames):
        write_data(new_videogames)
        return '', 204
    return jsonify({'message': 'Videogame not found'}), 404

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 3000))  
    app.run(host='0.0.0.0', port=port)

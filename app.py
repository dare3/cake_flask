from flask import Flask, jsonify, request, render_template
from models import db, Cupcake


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cupcakes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "alagbara-182"

db.init_app(app)

with app.app_context():
    db.create_all()  # Create the database and the cupcakes table

@app.route('/')
def index():
    return render_template('index.html')  # Render the HTML template

@app.route('/api/cupcakes', methods=['GET'])
def get_cupcakes():
    cupcakes = Cupcake.query.all()
    return jsonify({
        'cupcakes': [{
            'id': cupcake.id,
            'flavor': cupcake.flavor,
            'size': cupcake.size,
            'rating': cupcake.rating,
            'image': cupcake.image
        } for cupcake in cupcakes]
    })

@app.route('/api/cupcakes/<int:cupcake_id>', methods=['GET'])
def get_cupcake(cupcake_id):
    cupcake = Cupcake.query.get(cupcake_id)
    if cupcake is None:
        return jsonify({'error': 'Cupcake not found'}), 404

    return jsonify({
        'cupcake': {
            'id': cupcake.id,
            'flavor': cupcake.flavor,
            'size': cupcake.size,
            'rating': cupcake.rating,
            'image': cupcake.image
        }
    })

@app.route('/api/cupcakes', methods=['POST'])
def create_cupcake():
    data = request.json
    new_cupcake = Cupcake(
        flavor=data['flavor'],
        size=data['size'],
        rating=data['rating'],
        image=data.get('image', 'https://tinyurl.com/demo-cupcake')  # Default image if not provided
    )
    db.session.add(new_cupcake)
    db.session.commit()

    return jsonify({
        'cupcake': {
            'id': new_cupcake.id,
            'flavor': new_cupcake.flavor,
            'size': new_cupcake.size,
            'rating': new_cupcake.rating,
            'image': new_cupcake.image
        }
    }), 201

@app.route('/api/cupcakes/<int:cupcake_id>', methods=['PATCH'])
def update_cupcake(cupcake_id):
    cupcake = Cupcake.query.get(cupcake_id)
    if cupcake is None:
        return jsonify({'error': 'Cupcake not found'}), 404

    data = request.json
    cupcake.flavor = data['flavor']
    cupcake.size = data['size']
    cupcake.rating = data['rating']
    cupcake.image = data['image']
    
    db.session.commit()

    return jsonify({
        'cupcake': {
            'id': cupcake.id,
            'flavor': cupcake.flavor,
            'size': cupcake.size,
            'rating': cupcake.rating,
            'image': cupcake.image
        }
    })

@app.route('/api/cupcakes/<int:cupcake_id>', methods=['DELETE'])
def delete_cupcake(cupcake_id):
    cupcake = Cupcake.query.get(cupcake_id)
    if cupcake is None:
        return jsonify({'error': 'Cupcake not found'}), 404

    db.session.delete(cupcake)
    db.session.commit()
    
    return jsonify({'message': 'Deleted'})

if __name__ == '__main__':
    app.run(debug=True)

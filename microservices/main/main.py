from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint
from sqlalchemy.exc import IntegrityError
from producer import publish
import json
import requests

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234@172.18.0.2:5432/main_ms_flask_db'
# 172.21.0.2 ip on which db is running in the container

db = SQLAlchemy(app)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    title = db.Column(db.String(200))
    image = db.Column(db.String(200))

    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'image': self.image
        }

class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    product_id = db.Column(db.Integer)

    __table_args__ = (
        UniqueConstraint('user_id', 'product_id', name='unique_user_product'),
    )


@app.route('/api/products')
def index():
    products = db.session.query(Product).all()
    serialized_products = [product.serialize() for product in products]
    return jsonify(serialized_products)

@app.route('/api/products/<int:id>/like', methods=['GET'])
def like(id):
    req = requests.get('http://host.docker.internal:8000/api/users')
    json = req.json()

    try:
        # Start a transaction
        with db.session.begin():
            like = Like(user_id=json['id'], product_id=id)
            db.session.add(like)
            db.session.commit()
            publish('product_liked', id)

    except IntegrityError as e:
        return jsonify({
            'status': 'Error',
            'message': 'You have already liked this product'
        }), 400
    except Exception as e:
        # Rollback the transaction for other exceptions
        db.session.rollback()
        return jsonify({
            'status': 'Error',
            'message': str(e)
        }), 500

    return jsonify({
        'status': 'success',
        'message': 'You successfully liked this product!'
    })

if __name__=='__main__':
    app.run(debug=True, host='0.0.0.0')
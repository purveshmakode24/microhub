from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
import json

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


@app.route('/api/products')
def index():
    products = db.session.query(Product).all()
    serialized_products = [product.serialize() for product in products]
    return jsonify(serialized_products)

if __name__=='__main__':
    app.run(debug=True, host='0.0.0.0')
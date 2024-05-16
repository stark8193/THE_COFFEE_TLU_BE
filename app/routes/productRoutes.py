from flask import Blueprint, jsonify, request
from app.models import Product1
from app.schemas import ProductSchema
from app import db
#Bước 3
product_bp = Blueprint('product_bp', __name__)

product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

@product_bp.route('/product', methods=['POST'])
def add_product():
    data = request.get_json()
    name = data.get('name')
    description = data.get('description')
    price = data.get('price')
    qty = data.get('qty')

    new_product = Product1(name=name, description=description, price=price, qty=qty)

    db.session.add(new_product)
    db.session.commit()

    return product_schema.jsonify(new_product), 201  # Return with HTTP status 201 for created

@product_bp.route('/product', methods=['GET'])
def get_products():
    all_products = Product1.query.all()
    result = products_schema.dump(all_products)
    return jsonify(result)

@product_bp.route('/product/<int:id>', methods=['GET'])
def get_product(id):
    product = Product1.query.get_or_404(id)
    return product_schema.jsonify(product)

@product_bp.route('/product/<int:id>', methods=['PUT'])
def update_product(id):
    product = Product1.query.get_or_404(id)

    data = request.get_json()
    product.name = data.get('name', product.name)
    product.description = data.get('description', product.description)
    product.price = data.get('price', product.price)
    product.qty = data.get('qty', product.qty)

    db.session.commit()

    return product_schema.jsonify(product)

@product_bp.route('/product/<int:id>', methods=['DELETE'])
def delete_product(id):
    product = Product1.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()

    return product_schema.jsonify(product), 204  # Return with HTTP status 204 for no content

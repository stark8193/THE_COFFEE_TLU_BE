from flask import Blueprint, jsonify, request
from app.models import Product
from app.models import TypeProduct
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
    image = data.get('image')
    description = data.get('description')
    price = data.get('price')
    quantity = data.get('quantity')
    type_product_id = data.get('type_product_id')

    check_type_product_id = db.session.query(TypeProduct.id).filter_by(id=type_product_id).first() is not None
    check_name = db.session.query(Product.name).filter_by(name=name).first() is None
    check_image = db.session.query(Product.image).filter_by(image=image).first() is None

    if check_type_product_id and check_name and check_image:
        print('check_menu_id:',check_type_product_id)
        print('check_name:',check_name)
        new_product = Product(name=name, image=image, description=description
                              ,price=price,quantity=quantity, type_product_id=type_product_id)
        db.session.add(new_product)
        db.session.commit()
        return product_schema.jsonify(new_product), 200  # Return with HTTP status 201 for created
    else:
        return {
                'message': "Trùng tên hoặc link ảnh, hoặc ko tồn tại trong TypeProduct",
                'status': 400,
                'Error': 'ERR',
            }, 400

@product_bp.route('/product', methods=['GET'])
def get_products():
    all_products = Product.query.all()
    result = products_schema.dump(all_products)
    return jsonify(result), 200

@product_bp.route('/product/<int:id>', methods=['GET'])
def get_product(id):
    check = db.session.query(Product.id).filter_by(id=id).first() is not None
    if check:
        product = Product.query.get_or_404(id)
        return product_schema.jsonify(product),200
    else:
        return {
                'message': "KO tìm thấy bản ghi",
                'status': 400,
                'Error': 'ERR',
            }, 400
    
@product_bp.route('/product/<int:id>', methods=['PUT'])
def update_product(id):
    check = db.session.query(Product.id).filter_by(id=id).first() is not None
    if check:
        product = Product.query.get_or_404(id)
        data = request.get_json()
        check_type_product_id = db.session.query(TypeProduct.id).filter_by(id=data.get('type_product_id')).first() is not None
        check_name = db.session.query(Product.name).filter_by(name=data.get('name')).first() is None
        check_image = db.session.query(Product.image).filter_by(image=data.get('image')).first() is None
        if check_name and check_image and check_type_product_id:
            product.name = data.get('name')
            product.image = data.get('image')
            product.description = data.get('description')
            product.price = data.get('price')
            product.quantity = data.get('quantity')
            product.type_product_id = data.get('type_product_id')
            db.session.commit()
            return product_schema.jsonify(product),200
        else:
            return {
                'message': "Trùng tên hoặc link ảnh, hoặc ko tồn tại trong TypeProduct",
                'status': 400,
                'Error': 'ERR',
            }, 400

    else:
        return {
                'message': "KO tìm thấy bản ghi",
                'status': 400,
                'Error': 'ERR',
            }, 400

@product_bp.route('/product/<int:id>', methods=['DELETE'])
def delete_product(id):
    check = db.session.query(Product.id).filter_by(id=id).first() is not None
    if check:
        print('check:',check)
        product = Product.query.get_or_404(id)
        db.session.delete(product)
        db.session.commit()
        return{
                'message': 'Da xoa ban ghi',
                'status': 200,
            }, 200  # Return with HTTP status 204 for no content
    else:
        return {
                'message': "KO tim thay ban ghi",
                'status': 400,
                'Error': 'ERR',
            }, 400
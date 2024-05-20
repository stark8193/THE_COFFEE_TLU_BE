from flask import Blueprint, jsonify, request
from app.models import Topping, product, Product_Topping
from app.schemas import ProductSchema
from app.schemas import ToppingSchema
from app import db, app
from app.routes.productRoutes import product_bp

product_topping_bp = Blueprint('product_topping_bp', __name__)


topping_schema = ToppingSchema()
toppings_schema = ToppingSchema(many=True)
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)
@product_topping_bp.route('/product_topping', methods=['POST'])
def add_product_topping():
    data = request.json
    product_id = data['product_id']
    topping_id = data['topping_id']

    # Kiểm tra xem sản phẩm và topping tồn tại trong cơ sở dữ liệu
    Product = product.query.get(product_id)
    topping = Topping.query.get(topping_id)

    if Product is None:
        return jsonify({'message': 'Sản phẩm không tồn tại'}), 404

    if topping is None:
        return jsonify({'message': 'Topping không tồn tại'}), 404

    # Tạo một bản ghi mới trong bảng liên kết Product_Topping
    product_topping = Product_Topping.insert().values(idProduct=product_id, Topping_ID=topping_id)
    db.session.execute(product_topping)
    db.session.commit()

    return jsonify({'message': 'Liên kết sản phẩm và topping đã được tạo thành công'}), 201


# def add_topping_to_product(id):
#     data = request.get_json()
#     topping_id = data.get('Topping_ID')
#     if topping_id and id:
#         check_product_id = db.session.query(product.idProduct).filter_by(idProduct=id).first() is not None 
#         check_topping_id = db.session.query(Topping.Topping_ID).filter_by(Topping_ID=topping_id).first() is not None 
#         products = db.session.query(product.idProduct).filter_by(idProduct=id).first()
#         # print('product_topping:',products)             
#         if check_product_id and check_topping_id:
#             try:
#                 products.toppings.append(topping_id)
#                 db.session.commit()
#                 return {
#                     'message': 'Topping added to product successfully',
#                     'status': 200
#                 }, 200
#             except Exception as e:
#                 db.session.rollback()
#                 return {
#                     'message': 'Failed to add topping to product',
#                     'error': str(e),
#                     'status': 500
#                 }, 500
#         else:
#             return {
#                 'message': 'Product or Topping ko tìm thấy',
#                 'status': 404
#             }, 404
#     else:
#         return {
#             'message': 'Thiếu product ID or topping ID',
#             'status': 400
#         }, 400
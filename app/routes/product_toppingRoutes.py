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



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
    product_id = data['idProduct']
    topping_id = data['Topping_ID']

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

@product_topping_bp.route('/get_product_topping', methods=['GET'])
def get_product_topping():
    data = request.get_json()
    product_id = data.get('idProduct')
    if not product_id:
        return jsonify({"error": "idProduct is required"}), 400

    product_obj = product.query.filter_by(idProduct=product_id).first()

    if not product_obj:
        return jsonify({"error": "Product not found"}), 404

    toppings = product_obj.toppings

    # Serialize the toppings to JSON format
    toppings_list = []
    for topping in toppings:
        toppings_list.append({
            "Topping_ID": topping.Topping_ID,
            "Topping_Name": topping.Topping_Name,
            "Topping_Price": topping.Topping_Price
        })

    return jsonify({'data':toppings_list}), 200




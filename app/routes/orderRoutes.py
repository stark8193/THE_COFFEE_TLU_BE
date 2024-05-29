from flask import Blueprint, jsonify, request
from app.models import Order, Order_Detail, Topping_Addition, User, product
from app.schemas import OrderSchema, OrderDetailSchema, ToppingAdditionSchema
from flask_jwt_extended import jwt_required, get_jwt_identity

from app import db

order_bp = Blueprint('order_bp', __name__)

order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)

orderDetail_schema = OrderDetailSchema()
orderDetails_schema = OrderDetailSchema(many=True)

@order_bp.route('/add_order', methods=['POST'])
@jwt_required()
def add_order():
    data = request.get_json()
    current_user = get_jwt_identity()
    user = User.query.filter_by(User_Name=current_user).first()
    if not user:
        return jsonify(message="User not found"), 404
    user_id = user.User_ID
    
    product_id = data.get('idProduct')
    order_size = data.get('Order_Size')
    order_quantity = data.get('Order_Quantity')
    toppings = data.get('Toppings')  # List of toppings
    
    if not product_id or not order_size or not order_quantity:
        return jsonify(message="Product ID, Order Size, and Order Quantity are required"), 400
    
    existing_order = db.session.query(Order).filter_by(
        User_ID=user_id,
        Order_Status="Chưa xác nhận"
    ).first()
    
    if existing_order is None:
        try:
            new_order = Order(Order_Status="Chưa xác nhận", User_ID=user_id)
            db.session.add(new_order)
            db.session.commit()
            
            order_id = new_order.Order_ID
            add_order_details(order_id, product_id, order_size, order_quantity, toppings)
            
            return jsonify({'message': 'Order added successfully'}), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({'Error': 'ERR1', 'message': str(e)}), 500
    else:
        order_id = existing_order.Order_ID
        return add_product_to_existing_order(order_id, product_id, order_size, order_quantity, toppings)

def add_order_details(order_id, product_id, order_size, order_quantity, toppings):
    try:
        new_order_detail = Order_Detail(
            Order_Quantity=order_quantity,
            Order_ID=order_id,
            Order_Size=order_size,
            idProduct=product_id
        )
        db.session.add(new_order_detail)
        db.session.commit()
        
        if toppings and isinstance(toppings, list):
            order_detail_id = new_order_detail.Order_Detail_ID
            for topping in toppings:
                topping_name = topping.get('Topping_Addition_Name')
                topping_price = topping.get('Topping_Addition_Price')
                if topping_name and topping_price:
                    new_topping_addition = Topping_Addition(
                        Topping_Addition_Name=topping_name,
                        Topping_Addition_Price=topping_price,
                        Order_Detail_ID=order_detail_id
                    )
                    db.session.add(new_topping_addition)
            db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise

def add_product_to_existing_order(order_id, product_id, order_size, order_quantity, toppings):
    try:
        order_detail = db.session.query(Order_Detail).filter_by(
            idProduct=product_id,
            Order_ID=order_id
        ).first()
        
        if order_detail:
            if toppings:
                check_topping_name = all(
                    db.session.query(Topping_Addition).filter_by(
                        Order_Detail_ID=order_detail.Order_Detail_ID,
                        Topping_Addition_Name=topping['Topping_Addition_Name']
                    ).first() is not None for topping in toppings
                )
                if check_topping_name:
                    new_quantity = order_detail.Order_Quantity + order_quantity
                    order_detail.Order_Quantity = new_quantity
                    order_detail.Order_Size = order_size
                    db.session.commit()
                    return orderDetail_schema.jsonify(order_detail), 200
                else:
                    add_order_details(order_id, product_id, order_size, order_quantity, toppings)
                    return jsonify({"message": "Product with different toppings added to order successfully"}), 201
            else:
                new_quantity = order_detail.Order_Quantity + order_quantity
                order_detail.Order_Quantity = new_quantity
                order_detail.Order_Size = order_size
                db.session.commit()
                return orderDetail_schema.jsonify(order_detail), 200
        else:
            add_order_details(order_id, product_id, order_size, order_quantity, toppings)
            return jsonify({"message": "New product added to existing order successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'Error': 'ERR2', 'message': str(e)}), 500



''' đầu vào là Order_Detail_ID
    sửa số lượng, size và trong trường hợp  khi người dùng sửa topping đi, 
    ban đầu người ta chọn topping 1 2, nhưng sau đổi ý chọn topping 3 4 5
    (Vẫn phải nhập đủ 3 trường dữ liệu kể cả ko thay dổi vẫn giữ như cũ)'''
@order_bp.route('/update_order_detail/<string:id>', methods=['PUT'])
def update_order_detail(id):
    data = request.get_json()
    new_order_quantity = data.get('Order_Quantity')
    new_order_size = data.get('Order_Size')
    new_toppings = data.get('Toppings')  # List of new toppings

    try:
        order_detail = Order_Detail.query.get_or_404(id)
        
        if new_order_quantity is not None:
            order_detail.Order_Quantity = new_order_quantity

        if new_order_quantity is not None:
            order_detail.Order_Size = new_order_size
        
        if new_toppings and isinstance(new_toppings, list):
            existing_toppings = db.session.query(Topping_Addition).filter_by(Order_Detail_ID=id).first() is not None
            if existing_toppings:
                Topping_Addition.query.filter_by(Order_Detail_ID=id).delete()

            for topping in new_toppings:
                topping_name = topping.get('Topping_Addition_Name')
                topping_price = topping.get('Topping_Addition_Price')
                if topping_name and topping_price:
                    new_topping_addition = Topping_Addition(
                        Topping_Addition_Name=topping_name,
                        Topping_Addition_Price=topping_price,
                        Order_Detail_ID=id
                    )
                    db.session.add(new_topping_addition)
        
            db.session.commit()
        return jsonify({"message": "Order detail updated successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'Error': 'ERR7', 'message': str(e)}), 404


@order_bp.route('/delete_order/<string:id>', methods=['DELETE'])
def delete_order(id):
    try:
        order = Order.query.filter_by(Order_ID=id).first()
        if not order:
            return jsonify({'message': 'Order not found'}), 404
        
        order_details = Order_Detail.query.filter_by(Order_ID=id).all()

        for detail in order_details:
            toppings = Topping_Addition.query.filter_by(Order_Detail_ID=detail.Order_Detail_ID).all()
            for topping in toppings:
                db.session.delete(topping)
            
            db.session.delete(detail)
        
        db.session.delete(order)
        
        db.session.commit()

        return jsonify({'message': 'Order and related records deleted successfully'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'An error occurred while deleting the order', 'error': str(e)}), 500


@order_bp.route('/delete_order_detail/<string:id>', methods=['DELETE'])
def delete_order_detail(id):
    try:
        topping_additions_exist = db.session.query(Topping_Addition.Order_Detail_ID)\
            .filter_by(Order_Detail_ID=id).first() is not None
        order_detail = Order_Detail.query.get_or_404(id)
 
        if topping_additions_exist:
            print('Topping additions exist for order detail:', id)
            topping_additions = Topping_Addition.query.filter_by(Order_Detail_ID=id).all()
            for topping_addition in topping_additions:
                db.session.delete(topping_addition)

        db.session.delete(order_detail)
        db.session.commit()

        return {
            'message': 'Đã xóa bản ghi',
            'status': 200,
        }, 200  

    except Exception as e:
        db.session.rollback()
        return {
            'Error': 'ERR8',
            'message': str(e)
        }, 404
    
@order_bp.route('/update_order_status/<string:order_id>', methods=['PUT'])
@jwt_required()
def update_order_status(order_id):
    data = request.get_json()
    new_status = data.get('Order_Status')

    if not new_status:
        return jsonify({'Error': 'ERR1', 'message': 'Order status is required'}), 400

    try:
        order = Order.query.get_or_404(order_id)
        order.Order_Status = new_status
        db.session.commit()
        return jsonify({"message": "Order status updated successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'Error': 'ERR2', 'message': str(e)}), 500
@order_bp.route('/get_order_details', methods=['GET'])
@jwt_required()
def get_order_details():
    current_user = get_jwt_identity()
    user = User.query.filter_by(User_Name=current_user).first()
    if not user:
        return jsonify(message="User not found"), 404

    user_id = user.User_ID

    if not user_id:
        return jsonify({'error': 'User_ID is required'}), 400

    orders = db.session.query(
        Order.Order_ID,
        Order.Order_Date,
        Order.Order_Status,
        Order_Detail.Order_Detail_ID,
        Order_Detail.idProduct,
        Order_Detail.Order_Quantity,
        Order_Detail.Order_Size,
        product.Product_Price,
        product.Product_Name,  # Including Product_Name in the query
        Topping_Addition.Topping_Addition_Name,
        Topping_Addition.Topping_Addition_Price
    ).outerjoin(Order_Detail, Order.Order_ID == Order_Detail.Order_ID
    ).outerjoin(product, Order_Detail.idProduct == product.idProduct  # Joining with product table
    ).outerjoin(Topping_Addition, Order_Detail.Order_Detail_ID == Topping_Addition.Order_Detail_ID
    ).filter(Order.User_ID == user_id, Order.Order_Status == "Chưa xác nhận").all()  # Filtering orders by status

    # Dictionary to collect order details with the same Order_Detail_ID
    order_dict = {}

    for order in orders:
        order_detail_id = order.Order_Detail_ID

        # If Order_Detail_ID already exists in the dictionary, append details
        if order_detail_id in order_dict:
            order_dict[order_detail_id]['Toppings'].append({
                'Topping_Addition_Name': order.Topping_Addition_Name,
                'Topping_Addition_Price': order.Topping_Addition_Price
            })
        else:  # If Order_Detail_ID doesn't exist, create a new entry
            order_dict[order_detail_id] = {
                'Order_ID': order.Order_ID,
                'Order_Detail_ID': order_detail_id,
                'Order_Date': order.Order_Date,
                'Order_Status': order.Order_Status,
                'Order_Size': order.Order_Size,
                'idProduct': order.idProduct,
                'Product_Name': order.Product_Name,  # Adding Product_Name to the result
                'Product_Price': order.Product_Price,  
                'Order_Quantity': order.Order_Quantity,
                'Toppings': []  # Initialize list to store toppings
            }

            # Add toppings if available
            if order.Topping_Addition_Name and order.Topping_Addition_Price:
                order_dict[order_detail_id]['Toppings'].append({
                    'Topping_Addition_Name': order.Topping_Addition_Name,
                    'Topping_Addition_Price': order.Topping_Addition_Price
                })

    # Convert dictionary values to list to construct the final response
    order_list = list(order_dict.values())

    return jsonify({'data': order_list})



@order_bp.route('/get_order_detail_product/<string:id>', methods=['GET'])
@jwt_required()
def get_order_detail_product(id):
    current_user = get_jwt_identity()
    user = User.query.filter_by(User_Name=current_user).first()
    if not user:
        return jsonify(message="User not found"), 404
    user_id = user.User_ID
    
    if not user_id:
        return jsonify({'error': 'User_ID is required'}), 400
    orders = db.session.query(
        Order.Order_ID,
        Order.Order_Date,
        Order.Order_Status,
        Order_Detail.Order_Detail_ID,
        Order_Detail.idProduct,
        Order_Detail.Order_Quantity,
        Order_Detail.Order_Size,
        product.Product_Name,  
        product.Product_Price,
        Topping_Addition.Topping_Addition_Name,
        Topping_Addition.Topping_Addition_Price
    ).outerjoin(Order_Detail, Order.Order_ID == Order_Detail.Order_ID
    ).outerjoin(product, Order_Detail.idProduct == product.idProduct
    ).outerjoin(Topping_Addition, Order_Detail.Order_Detail_ID == Topping_Addition.Order_Detail_ID
    ).filter(Order.User_ID == user_id,
             Order.Order_Status == "Chưa xác nhận",
             Order_Detail.idProduct == id).all()

    # Construct response
    order_details = {}
    for order in orders:
        order_detail_id = order.Order_Detail_ID
        if order_detail_id not in order_details:
            order_details[order_detail_id] = {
                'Order_Date': order.Order_Date.strftime("%a, %d %b %Y %H:%M:%S GMT"),
                'Order_Detail_ID': order.Order_Detail_ID,
                'Order_ID': order.Order_ID,
                'Order_Quantity': order.Order_Quantity,
                'Order_Size': order.Order_Size,
                'Order_Status': order.Order_Status,
                'Product_Name': order.Product_Name,
                'idProduct': order.idProduct,
                'Product_Price':order.Product_Price,
                'Toppings': []
            }
        order_details[order_detail_id]['Toppings'].append({
            'Topping_Addition_Name': order.Topping_Addition_Name,
            'Topping_Addition_Price': order.Topping_Addition_Price
        })

    return jsonify({"data":list(order_details.values())})
@order_bp.route('/get_all_order_details', methods=['GET'])
@jwt_required()
def get_all_order_details():
    orders = db.session.query(
        Order.Order_ID,
        Order.Order_Date,
        Order.Order_Status,
        Order.User_ID,
        Order_Detail.Order_Detail_ID,
        Order_Detail.idProduct,
        Order_Detail.Order_Quantity,
        Order_Detail.Order_Size,
        product.Product_Price,
        product.Product_Name,
        Topping_Addition.Topping_Addition_Name,
        Topping_Addition.Topping_Addition_Price
    ).outerjoin(Order_Detail, Order.Order_ID == Order_Detail.Order_ID
    ).outerjoin(product, Order_Detail.idProduct == product.idProduct
    ).outerjoin(Topping_Addition, Order_Detail.Order_Detail_ID == Topping_Addition.Order_Detail_ID
    ).all()

    orders_dict = {}

    for order in orders:
        order_id = order.Order_ID
        order_detail_id = order.Order_Detail_ID

        # If Order_ID already exists in the dictionary, append order details
        if order_id in orders_dict:
            order_detail = {
                'Order_Detail_ID': order_detail_id,
                'Order_Quantity': order.Order_Quantity,
                'Order_Size': order.Order_Size,
                'Product_Name': order.Product_Name,
                'Product_Price': order.Product_Price,
            }

            # If Order_Detail_ID already exists, append toppings
            if order_detail_id in orders_dict[order_id]['Order_Details']:
                orders_dict[order_id]['Order_Details'][order_detail_id]['Toppings'].append({
                    'Topping_Addition_Name': order.Topping_Addition_Name,
                    'Topping_Addition_Price': order.Topping_Addition_Price
                })
            else:
                order_detail['Toppings'] = [{
                    'Topping_Addition_Name': order.Topping_Addition_Name,
                    'Topping_Addition_Price': order.Topping_Addition_Price
                }]
                orders_dict[order_id]['Order_Details'][order_detail_id] = order_detail
        else:
            order_dict = {
                'Order_ID': order_id,
                'Order_Date': order.Order_Date,
                'Order_Status': order.Order_Status,
                'User_ID': order.User_ID,
                'Order_Details': {
                    order_detail_id: {
                        'Order_Detail_ID': order_detail_id,
                        'Order_Quantity': order.Order_Quantity,
                        'Order_Size': order.Order_Size,
                        'Product_Name': order.Product_Name,
                        'Product_Price': order.Product_Price,
                        'Toppings': [{
                            'Topping_Addition_Name': order.Topping_Addition_Name,
                            'Topping_Addition_Price': order.Topping_Addition_Price
                        }]
                    }
                }
            }
            orders_dict[order_id] = order_dict

    order_list = list(orders_dict.values())

    return jsonify({'data': order_list})

from flask import Blueprint, jsonify, request, url_for, redirect
from sqlalchemy.orm import aliased
from app.models import Order, Order_Detail, Topping_Addition, User
from app.schemas import OrderSchema, OrderDetailSchema, ToppingAdditionSchema
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity, get_jwt

from app import db, app

order_bp = Blueprint('order_bp', __name__)

order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)

orderDetail_schema = OrderDetailSchema()
orderDetails_schema = OrderDetailSchema(many=True)

'''TH1: chưa có order nào hoặc có order đã xác nhận
        thì thêm mới order đồng thời thêm mới order_detail vs topping_addition luôn
    Tất cả đều là nhiều topping
   {
    "User_ID": "bf0886e9-810f-424a-acd2-d1cd8b62a368",
    "idProduct": "0zvuaigyslst47jtd",
    "Order_Size":"Lớn",
    "Order_Quantity": 2,
    "Toppings": [
        {
            "Topping_Addition_Name": "test1",
            "Topping_Addition_Price": 1
        },
        {
            "Topping_Addition_Name": "test2",
            "Topping_Addition_Price": 1.5
        }
    ]}
'''
@order_bp.route('/add_order', methods=['POST'])
def add_order():
    data = request.get_json()
    # user_id = data.get('User_ID')
    current_user = get_jwt_identity()
    user = User.query.filter_by(User_Name=current_user).first()
    if not user:
        return jsonify(message="User not found"), 404
    user_id = user.User_ID
    product_id = data.get('idProduct')
    order_size = data.get('Order_Size')
    order_quantity = data.get('Order_Quantity')
    toppings = data.get('Toppings')  # List of toppings
    
    if user_id:
        check_order_status = db.session.query(Order).filter_by(
            User_ID=user_id,
            Order_Status="Chưa xác nhận"
        ).first() is None
        print("check_order_status:",check_order_status)
        if check_order_status:
            try:
                new_order = Order(Order_Status="Chưa xác nhận", User_ID=user_id)
                db.session.add(new_order)
                db.session.commit()
                
                order_id = new_order.Order_ID
                new_order_detail = Order_Detail(
                    Order_Quantity=order_quantity,
                    Order_ID=order_id,
                    Order_Size= order_size,
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

                return jsonify({'Mess':'Them thanh cong'}), 201
            except Exception as e:
                db.session.rollback()
                return jsonify({'Error': 'ERR1', 'message': str(e)}), 404
        else:
            return redirect(url_for('order_bp.add_product'))
    else:
        return jsonify({
            'message': "Thiếu User_ID",
            'status': 400,
            'Error': 'ERR2',
        }), 400

'''Chỉ cần gọi /add_order nó tự chạy vào đây
    TH2: có order chưa xác nhận muốn thêm cùng sản phẩm 
   cùng loại topping (tức là chỉ thay đổi số lượng, size) thì thay đổi mỗi số lượng,size
   TH3: có order chưa xác nhận muốn thêm cùng sản phẩm (hoặc khác sp) 
   và khác topping thì thêm mới sp đó vs topping khác hoặc ko toppping
   
   Tất cả đều là nhiều topping
   {
    "User_ID": "bf0886e9-810f-424a-acd2-d1cd8b62a368",
    "idProduct": "0zvuaigyslst47jtd",
    "Order_Size":"Lớn",
    "Order_Quantity": 2,
    "Toppings": [
        {
            "Topping_Addition_Name": "test1",
            "Topping_Addition_Price": 1
        },
        {
            "Topping_Addition_Name": "test2",
            "Topping_Addition_Price": 1.5
        }
    ]}
'''
@order_bp.route('/add_product', methods=['POST'])  
def add_product():
    data = request.get_json()
    user_id = data.get('User_ID')
    order = db.session.query(Order).filter_by(
        User_ID=user_id,
        Order_Status="Chưa xác nhận"
    ).first()
    
    if order:
        print('order_id:', order.Order_ID)
        product_id = data.get('idProduct')
        order_quantity = data.get('Order_Quantity')
        order_size = data.get('Order_Size')
        toppings = data.get('Toppings')  # List of toppings

        order_detail = db.session.query(Order_Detail).filter_by(
            idProduct=product_id,
            Order_ID=order.Order_ID
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
                    print('check_topping_name',check_topping_name)
                    try:
                        new_quantity = order_detail.Order_Quantity + order_quantity
                        order_detail.Order_Quantity = new_quantity
                        order_detail.Order_Size = order_size
                        db.session.commit()
                        return orderDetail_schema.jsonify(order_detail), 200
                    except Exception as e:
                        db.session.rollback()
                        return jsonify({'Error': 'ERR3', 'message': str(e)}), 404
                else:
                    try:
                        new_order_detail = Order_Detail(
                            Order_Quantity=order_quantity,
                            Order_ID=order.Order_ID,
                            Order_Size= order_size,
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
                            
                        return jsonify({"message": "Product added to order successfully"}), 201
                    except Exception as e:
                        db.session.rollback()
                        return jsonify({'Error': 'ERR4', 'message': str(e)}), 404
            else:
                try:
                    new_order_detail_no_topping = Order_Detail(
                                Order_Quantity=order_quantity,
                                Order_ID=order.Order_ID,
                                Order_Size= order_size,
                                idProduct=product_id
                            )
                    db.session.add(new_order_detail_no_topping)
                    db.session.commit()
                    return jsonify({"message": "Product added to order successfully"}), 201
                except Exception as e:
                        db.session.rollback()
                        return jsonify({'Error': 'ERR5', 'message': str(e)}), 404
    else:
        return jsonify({'Error': 'ERR6'}), 404

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



@order_bp.route('/delete_order_detail/<string:id>', methods=['DELETE'])
def delete_order_detail(id):
    try:
        topping_additions_exist = db.session.query(Topping_Addition.Order_Detail_ID).filter_by(Order_Detail_ID=id).first() is not None

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

     

@order_bp.route('/get_order_details', methods=['GET'])
def get_order_details():
    data = request.get_json()
    user_id = data.get('User_ID')
    
    if not user_id:
        return jsonify({'error': 'User_ID is required'}), 400

    orders = db.session.query(
        Order.Order_ID,
        Order.Order_Date,
        Order.Order_Status,
        Order_Detail.Order_Detail_ID,
        Order_Detail.idProduct,
        Order_Detail.Order_Quantity,
        Topping_Addition.Topping_Addition_Name,
        Topping_Addition.Topping_Addition_Price
    ).outerjoin(Order_Detail, Order.Order_ID == Order_Detail.Order_ID
    ).outerjoin(Topping_Addition, Order_Detail.Order_Detail_ID == Topping_Addition.Order_Detail_ID
    ).filter(Order.User_ID == user_id).all()

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
                'idProduct': order.idProduct,
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

    return jsonify({'data':order_list})


from flask import Blueprint, jsonify, request, url_for, redirect
from sqlalchemy.orm import aliased
from app.models import Order, Order_Detail, Topping_Addition, product
from app.schemas import OrderSchema, OrderDetailSchema, ToppingAdditionSchema
from app import db, app

order_bp = Blueprint('order_bp', __name__)

order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)

orderDetail_schema = OrderDetailSchema()
orderDetails_schema = OrderDetailSchema(many=True)

@order_bp.route('/add_order', methods=['POST'])
def add_order():
    data = request.get_json()
    user_id = data.get('User_ID')
    product_id = data.get('idProduct')
    order_quantity = data.get('Order_Quantity')
    topping_addition_name = data.get('Topping_Addition_Name')
    topping_addition_price = data.get('Topping_Addition_Price')
    
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
                    idProduct=product_id
                )
                db.session.add(new_order_detail)
                db.session.commit()
                
                if topping_addition_name and topping_addition_price:
                    order_detail_id = new_order_detail.Order_Detail_ID
                    new_topping_addition = Topping_Addition(
                        Topping_Addition_Name=topping_addition_name,
                        Topping_Addition_Price=topping_addition_price,
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
            # return jsonify({'Error': 'ERR10', 'message': str(e)}), 404
    else:
        return jsonify({
            'message': "Thiếu User_ID",
            'status': 400,
            'Error': 'ERR2',
        }), 400

@order_bp.route('/add_product', methods=['POST'])
def add_product():
    data = request.get_json()
    user_id = data.get('User_ID')
    order_id = db.session.query(Order).filter_by(
        User_ID=user_id,
        Order_Status="Chưa xác nhận"
    ).first()
    print('order_id ở đây 2:',order_id.Order_ID)
    if order_id:
        product_id = data.get('idProduct')
        order_quantity = data.get('Order_Quantity')
        topping_addition_name = data.get('Topping_Addition_Name')
        topping_addition_price = data.get('Topping_Addition_Price')
        check_product_id = db.session.query(Order_Detail).filter_by(
            idProduct=product_id,
            Order_ID=order_id.Order_ID
        ).first() is not None

        order_detail_id_old = Order_Detail.query.filter_by(
            idProduct=product_id,
            Order_ID=order_id.Order_ID
        ).first()

        check_topping_name = db.session.query(Topping_Addition).filter_by(
            Order_Detail_ID=order_detail_id_old.Order_Detail_ID,
            Topping_Addition_Name=topping_addition_name
        ).first() is not None

        if (check_product_id and check_topping_name):
            print("11111")
            try:
                # print('order_detail_id:',order_detail_id_old.Order_Detail_ID)
                product_order_detail_update = Order_Detail.query.get_or_404(order_detail_id_old.Order_Detail_ID)
                new_quantity = order_detail_id_old.Order_Quantity + order_quantity
                # print('new_quantity',new_quantity)
                product_order_detail_update.Order_Quantity = new_quantity
                db.session.commit()
                return orderDetail_schema.jsonify(product_order_detail_update),200
            except Exception as e:
                db.session.rollback()
                return jsonify({'Error': 'ERR3', 'message': str(e)}), 404
        else: 
            try:
                new_order_detail = Order_Detail(
                    Order_Quantity=order_quantity,
                    Order_ID=order_id.Order_ID,  
                    idProduct=product_id
                )
                db.session.add(new_order_detail)
                db.session.commit()
                
                if topping_addition_name and topping_addition_price:
                    order_detail_id = new_order_detail.Order_Detail_ID
                    new_topping_addition = Topping_Addition(
                        Topping_Addition_Name=topping_addition_name,
                        Topping_Addition_Price=topping_addition_price,
                        Order_Detail_ID=order_detail_id
                    )
                    db.session.add(new_topping_addition)
                    db.session.commit()
                    
                return jsonify({"message": "Product added to order successfully"}), 201
            except Exception as e:
                db.session.rollback()
                return jsonify({'Error': 'ERR5', 'message': str(e)}), 404
    else:
        return jsonify({'Error': 'ERR5'}), 404

@order_bp.route('/delete_order_detail/<string:id>', methods=['DELETE'])
def delete_order_detail(id):
    check = db.session.query(Topping_Addition.Order_Detail_ID).filter_by(Order_Detail_ID=id).first() is not None
    if check:
        print('check:',check)
        try:
            order_detail = Order_Detail.query.get_or_404(id)
            topping_additions = Topping_Addition.query.filter_by(Order_Detail_ID=id).all()
            for topping_addition in topping_additions:
                db.session.delete(topping_addition)
            db.session.delete(order_detail)
            db.session.commit()
            return{
                    'message': 'Đã xóa bản ghi',
                    'status': 200,
                }, 200  # Return with HTTP status 204 for no content
        except:
            return {
                'Error': 'ERR1',
            },404
    else:
        try:
            # topping_addition = Topping_Addition.query.get_or_404(id)
            order_detail = Order_Detail.query.get_or_404(id)
            # db.session.delete(topping_addition)
            db.session.delete(order_detail)
            db.session.commit()
            return{
                    'message': 'Đã xóa bản ghi',
                    'status': 200,
                }, 200  # Return with HTTP status 204 for no content
        except:
            return {
                'Error': 'ERR2',
            },404
     

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

    order_list = []
    for order in orders:
        order_dict = {
            'Order_ID': order.Order_ID,
            'Order_Date': order.Order_Date,
            'Order_Status': order.Order_Status,
            'Order_Detail_ID': order.Order_Detail_ID if order.Order_Detail_ID else '',
            'idProduct': order.idProduct if order.idProduct else '',
            'Order_Quantity': order.Order_Quantity if order.Order_Quantity else '',
            'Topping_Addition_Name': order.Topping_Addition_Name if order.Topping_Addition_Name else '',
            'Topping_Addition_Price': order.Topping_Addition_Price if order.Topping_Addition_Price else ''
        }
        order_list.append(order_dict)

    return jsonify(order_list)

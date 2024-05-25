from flask import Blueprint, jsonify, request
from app.models import Topping
from app.schemas import ToppingSchema
from app import db
#Bước 3
topping_bp = Blueprint('topping_bp', __name__)

topping_schema = ToppingSchema()
toppings_schema = ToppingSchema(many=True)

@topping_bp.route('/topping', methods=['POST'])
def add_topping():
    data = request.get_json()
    name = data.get('Topping_Name')
    price = data.get('Topping_Price')
    if name and price:
        check_name = db.session.query(Topping.Topping_Name).filter_by(Topping_Name=name).first() is None

        if check_name:
            print('check_name:',check_name)
            try:
                new_topping = Topping(Topping_Name=name,Topping_Price=price)
                db.session.add(new_topping)
                db.session.commit()
                return topping_schema.jsonify(new_topping), 200  # Return with HTTP status 201 for created
            except:
                return {
                    'Error': 'ERR',
                },404
        else:
            return {
                    'message': "Trùng tên",
                    'status': 400,
                    'Error': 'ERR',
                }, 400
    else:
        return {
                    'message': "Nhập thiếu dữ liệu",
                    'status': 400,
                    'Error': 'ERR',
                }, 400

@topping_bp.route('/topping', methods=['GET'])
def get_toppings():
    try:
        all_toppings = Topping.query.all()
        result = toppings_schema.dump(all_toppings)
        return jsonify({'data':result}), 200
    except:
        return {
            'Error': 'ERR',
        },404

@topping_bp.route('/topping/<string:id>', methods=['GET'])
def get_topping(id):
    check = db.session.query(Topping.Topping_ID).filter_by(Topping_ID=id).first() is not None
    if check:
        try: 
            topping_get_by_id = Topping.query.get_or_404(id)
            return topping_schema.jsonify(topping_get_by_id),200
        except:
            return {
                'Error': 'ERR',
            },404
    else:
        return {
                'message': "KO tìm thấy bản ghi",
                'status': 400,
                'Error': 'ERR',
            }, 400
    
@topping_bp.route('/topping/<string:id>', methods=['PUT'])
def update_topping(id):
    check = db.session.query(Topping.Topping_ID).filter_by(Topping_ID=id).first() is not None
    if check:
        try:
            topping_update = Topping.query.get_or_404(id)
            data = request.get_json()
            name = data.get('Topping_Name')
            price = data.get('Topping_Price')
            if name and price:
                check_name = db.session.query(Topping.Topping_Name).filter_by(Topping_Name=name).first() is None
                if check_name:
                    topping_update.Topping_Name = name
                    topping_update.Topping_Price = price
                    db.session.commit()
                    return topping_schema.jsonify(topping_update),200
                else:
                    return {
                        'message': "Trùng tên",
                        'status': 400,
                        'Error': 'ERR',
                    }, 400
            else:
                return {
                            'message': "Nhập thiếu dữ liệu",
                            'status': 400,
                            'Error': 'ERR',
                        }, 400
        except:
            return {
                'Error': 'ERR',
            },404
    else:
        return {
                'message': "KO tìm thấy bản ghi",
                'status': 400,
                'Error': 'ERR',
            }, 400

@topping_bp.route('/topping/<string:id>', methods=['DELETE'])
def delete_topping(id):
    check = db.session.query(Topping.Topping_ID).filter_by(Topping_ID=id).first() is not None
    if check:
        print('check:',check)
        try:
            topping_delete = Topping.query.get_or_404(id)
            db.session.delete(topping_delete)
            db.session.commit()
            return{
                    'message': 'Da xoa ban ghi',
                    'status': 200,
                }, 200  # Return with HTTP status 204 for no content
        except:
            return {
                'Error': 'ERR',
            },404
    else:
        return {
                'message': "KO tim thay ban ghi",
                'status': 400,
                'Error': 'ERR',
            }, 400

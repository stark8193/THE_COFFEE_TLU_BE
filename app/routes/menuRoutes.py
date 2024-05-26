from flask import Blueprint, jsonify, request
from app.models import Menu
from app.schemas import MenuSchema
from app import db
#Bước 3
menu_bp = Blueprint('Menu_bp', __name__)

menu_schema = MenuSchema()
menus_schema = MenuSchema(many=True)

@menu_bp.route('/menu', methods=['POST'])
def add_menu():
    data = request.get_json()
    name = data.get('Name_Menu')
    if name:
        print('name:',name)
        check = db.session.query(Menu.Name_Menu).filter_by(Name_Menu=name).first() is None
        if check:
            print('check:',check)
            try: 
                new_menu = Menu(Name_Menu=name)
                db.session.add(new_menu)
                db.session.commit()
                menu_data = {
                    'Name_Menu':new_menu.Name_Menu,
                    'Menu_ID':new_menu.Menu_ID
                    
                }
                return jsonify({'data':menu_data}), 200  # Return with HTTP status 201 for created
            except:
                return {
                    'Error': 'ERR',
                },404
        else:
            return {
                    'message': "Bản ghi đã tồn tại",
                    'status': 400,
                    'Error': 'ERR',
                }, 400
    else:
        return {
                    'message': "Nhập thiếu dữ liệu",
                    'status': 400,
                    'Error': 'ERR',
                }, 400

@menu_bp.route('/menu', methods=['GET'])
def get_menus():
    try:
        all_menus = Menu.query.all()
        result = menus_schema.dump(all_menus)
        return jsonify({"data":result}),200
    except:
        return {
            'Error': 'ERR',
        },404

@menu_bp.route('/menu/<string:id>', methods=['GET'])
def get_menu(id):
    check = db.session.query(Menu.Menu_ID).filter_by(Menu_ID = id).first() is not None
    if check:
        try: 
            menu = Menu.query.get_or_404(id)
            # return menu_schema.jsonify(menu),200
            result = menu_schema.dump(menu)
            return jsonify({"data": [result]}), 200
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

@menu_bp.route('/menu/<string:id>', methods=['PUT'])
def update_menu(id):
    check_id = db.session.query(Menu.Menu_ID).filter_by(Menu_ID=id).first() is not None
    if check_id:
        print("check_id:",check_id)
        try: 
            menu = Menu.query.get_or_404(id)
            data = request.get_json()
            name=data.get('Name_Menu')
            if name:
                check_name = db.session.query(Menu.Name_Menu).filter_by(Name_Menu=name).first() is None
                if check_name:
                    menu.Name_Menu = name
                    db.session.commit()
                    return menu_schema.jsonify(menu),200
                else:
                    return {
                        'message': "trung ten ban ghi",
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
                'message': "KO tim thay ban ghi",
                'status': 400,
                'Error': 'ERR',
            }, 400

@menu_bp.route('/menu/<string:id>', methods=['DELETE'])
def delete_menu(id):
    check = db.session.query(Menu.Menu_ID).filter_by(Menu_ID=id).first() is not None
    if check:
        print('check:',check)
        try:
            menu = Menu.query.get_or_404(id)
            db.session.delete(menu)
            db.session.commit()
            return{
                    'message': 'Đã xóa bản ghi',
                    'status': 200,
                }, 200  # Return with HTTP status 204 for no content
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
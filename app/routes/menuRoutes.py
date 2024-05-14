from flask import Blueprint, jsonify, request
from app.models import Menu
from app.schemas import MenuSchema
from app import db
#Bước 3
menu_bp = Blueprint('Menu_bp', __name__)

menu_schema = MenuSchema()
menus_schema = MenuSchema(many=True)

@menu_bp.route('/menu', methods=['POST'])
def add_product():
    data = request.get_json()
    name = data.get('name')
    check = db.session.query(Menu.name).filter_by(name=name).first() is None
    if check:
        print('check:',check)
        new_menu = Menu(name=name)
        db.session.add(new_menu)
        db.session.commit()
        return menu_schema.jsonify(new_menu), 200  # Return with HTTP status 201 for created
    else:
        return {
                'message': "ban ghi da ton tai",
                'status': 400,
                'Error': 'ERR',
            }, 400


@menu_bp.route('/menu', methods=['GET'])
def get_menus():
    all_menus = Menu.query.all()
    result = menus_schema.dump(all_menus)
    return jsonify(result),200

@menu_bp.route('/menu/<int:id>', methods=['GET'])
def get_menu(id):
    check = db.session.query(Menu.id).filter_by(id=id).first() is not None
    if check:
        menu = Menu.query.get_or_404(id)
        return menu_schema.jsonify(menu),200
    else:
        return {
                'message': "KO tim thay ban ghi",
                'status': 400,
                'Error': 'ERR',
            }, 400

@menu_bp.route('/menu/<int:id>', methods=['PUT'])
def update_menu(id):
    check_id = db.session.query(Menu.id).filter_by(id=id).first() is not None
    if check_id:
        menu = Menu.query.get_or_404(id)
        data = request.get_json()
        check_name = db.session.query(Menu.name).filter_by(name=data.get('name')).first() is None
        if check_name:
            menu.name = data.get('name')
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
                'message': "KO tim thay ban ghi",
                'status': 400,
                'Error': 'ERR',
            }, 400

@menu_bp.route('/menu/<int:id>', methods=['DELETE'])
def delete_menu(id):
    check = db.session.query(Menu.id).filter_by(id=id).first() is not None
    if check:
        print('check:',check)
        menu = Menu.query.get_or_404(id)
        db.session.delete(menu)
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
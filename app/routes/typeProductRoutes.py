from flask import Blueprint, jsonify, request
from app.models import TypeProduct
from app.models import Menu
from app.schemas import TypeProductSchema
from app import db
#Bước 3
typeProduct_bp = Blueprint('typeProduct_bp', __name__)

typeProduct_schema = TypeProductSchema()
typeProducts_schema = TypeProductSchema(many=True)

@typeProduct_bp.route('/typeProduct', methods=['POST'])
def add_typeProduct():
    data = request.get_json()
    name = data.get('name')
    image = data.get('image')
    menu_id = data.get('menu_id')
    check_menu_id = db.session.query(Menu.id).filter_by(id=menu_id).first() is not None
    check_name = db.session.query(TypeProduct.name).filter_by(name=name).first() is None
    check_image = db.session.query(TypeProduct.image).filter_by(image=image).first() is None
    if check_menu_id and check_name and check_image:
        print('check_menu_id:',check_menu_id)
        print('check_name:',check_name)
        new_typeProduct = TypeProduct(name=name, image=image, menu_id=menu_id)
        db.session.add(new_typeProduct)
        db.session.commit()
        return typeProduct_schema.jsonify(new_typeProduct), 200  # Return with HTTP status 201 for created
    else:
        return {
                'message': "Trùng tên hoặc link ảnh, hoặc ko tồn tại trong Menu",
                'status': 400,
                'Error': 'ERR',
            }, 400

@typeProduct_bp.route('/typeProduct', methods=['GET'])
def get_typeProducts():
    all_typeProducts = TypeProduct.query.all()
    result = typeProducts_schema.dump(all_typeProducts)
    return jsonify(result), 200

@typeProduct_bp.route('/typeProduct/<int:id>', methods=['GET'])
def get_typeProduct(id):
    check = db.session.query(TypeProduct.id).filter_by(id=id).first() is not None
    if check:
        typeProduct = TypeProduct.query.get_or_404(id)
        return typeProduct_schema.jsonify(typeProduct),200
    else:
        return {
                'message': "KO tim thay ban ghi",
                'status': 400,
                'Error': 'ERR',
            }, 400
    
@typeProduct_bp.route('/typeProduct/<int:id>', methods=['PUT'])
def update_typeProduct(id):
    check = db.session.query(TypeProduct.id).filter_by(id=id).first() is not None
    if check:
        typeProduct = TypeProduct.query.get_or_404(id)
        data = request.get_json()
        check_menu_id = db.session.query(Menu.id).filter_by(id=data.get('menu_id')).first() is not None
        check_name = db.session.query(TypeProduct.name).filter_by(name=data.get('name')).first() is None
        check_image = db.session.query(TypeProduct.image).filter_by(image=data.get('image')).first() is None
        if check_name and check_image and check_menu_id:
            typeProduct.name = data.get('name')
            typeProduct.image = data.get('image')
            typeProduct.menu_id = data.get('menu_id')
            db.session.commit()
            return typeProduct_schema.jsonify(typeProduct),200
        else:
            return {
                'message': "name, image bi trung hoac khong ton tai trong menu",
                'status': 400,
                'Error': 'ERR',
            }, 400

    else:
        return {
                'message': "KO tim thay ban ghi",
                'status': 400,
                'Error': 'ERR',
            }, 400

@typeProduct_bp.route('/typeProduct/<int:id>', methods=['DELETE'])
def delete_typeProduct(id):
    check = db.session.query(TypeProduct.id).filter_by(id=id).first() is not None
    if check:
        print('check:',check)
        typeProduct = TypeProduct.query.get_or_404(id)
        db.session.delete(typeProduct)
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
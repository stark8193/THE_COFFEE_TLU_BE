from flask import Blueprint, jsonify, request
from app.models import typeproduct
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
    name = data.get('TypeProduct_Name')
    image = data.get('TypeProduct_Img')
    menu_id = data.get('Menu_ID')
    if name and image and menu_id:
        check_menu_id = db.session.query(Menu.Menu_ID).filter_by(Menu_ID=menu_id).first() is not None
        check_name = db.session.query(typeproduct.TypeProduct_Name).filter_by(TypeProduct_Name=name).first() is None
        check_image = db.session.query(typeproduct.TypeProduct_Img).filter_by(TypeProduct_Img=image).first() is None
        if check_menu_id and check_name and check_image:
            try:
                print('check_menu_id:',check_menu_id)
                print('check_name:',check_name)
                new_typeProduct = typeproduct(TypeProduct_Name=name, TypeProduct_Img=image, Menu_ID=menu_id)
                db.session.add(new_typeProduct)
                db.session.commit()
                return typeProduct_schema.jsonify(new_typeProduct), 200  # Return with HTTP status 201 for created
            except:
                return {
                    'Error': 'ERR',
                },404
        else:
            return {
                    'message': "Trùng tên hoặc link ảnh, hoặc ko tồn tại trong Menu",
                    'status': 400,
                    'Error': 'ERR',
                }, 400
    else:
        return {
                    'message': "Nhập thiếu dữ liệu",
                    'status': 400,
                    'Error': 'ERR',
                }, 400

@typeProduct_bp.route('/typeProduct', methods=['GET'])
def get_typeProducts():
    try:
        all_typeProducts = typeproduct.query.all()
        result = typeProducts_schema.dump(all_typeProducts)
        return jsonify(result), 200
    except:
        return {
            'Error': 'ERR',
        },404
    
@typeProduct_bp.route('/typeProduct/<string:id>', methods=['GET'])
def get_typeProduct(id):
    check = db.session.query(typeproduct.TypeProduct_ID).filter_by(TypeProduct_ID=id).first() is not None
    if check:
        print('check:',check)
        try:
            typeproduct_get_by_id = typeproduct.query.get_or_404(id)
            return typeProduct_schema.jsonify(typeproduct_get_by_id),200
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
    
@typeProduct_bp.route('/typeProduct/<string:id>', methods=['PUT'])
def update_typeProduct(id):
    check = db.session.query(typeproduct.TypeProduct_ID).filter_by(TypeProduct_ID=id).first() is not None
    if check:
        try:
            typeProduct_update = typeproduct.query.get_or_404(id)
            data = request.get_json()
            name = data.get('TypeProduct_Name')
            image = data.get('TypeProduct_Img')
            menu_id = data.get('Menu_ID')
            if name and image and menu_id:
                check_menu_id = db.session.query(Menu.Menu_ID).filter_by(Menu_ID=menu_id).first() is not None
                check_name = db.session.query(typeproduct.TypeProduct_Name).filter_by(TypeProduct_Name=name).first() is None
                check_image = db.session.query(typeproduct.TypeProduct_Img).filter_by(TypeProduct_Img=image).first() is None
                if check_name and check_image and check_menu_id:
                    typeProduct_update.TypeProduct_Name = name
                    typeProduct_update.TypeProduct_Img = image
                    typeProduct_update.Menu_ID = menu_id
                    db.session.commit()
                    return typeProduct_schema.jsonify(typeProduct_update),200
                else:
                    return {
                        'message': "name, image bi trung hoac khong ton tai trong menu",
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

@typeProduct_bp.route('/typeProduct/<string:id>', methods=['DELETE'])
def delete_typeProduct(id):
    check = db.session.query(typeproduct.TypeProduct_ID).filter_by(TypeProduct_ID=id).first() is not None
    if check:
        print('check:',check)
        try: 
            typeProduct_delete = typeproduct.query.get_or_404(id)
            db.session.delete(typeProduct_delete)
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
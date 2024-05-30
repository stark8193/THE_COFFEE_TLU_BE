from flask import Blueprint, jsonify, request
from app.models import typenews
from app.schemas import TypeNewsSchema
from app import db

#Bước 3
typenews_bp = Blueprint('typenews_bp', __name__)

typenews_schema = TypeNewsSchema()
typenewses_schema = TypeNewsSchema(many=True)

@typenews_bp.route('/typenews', methods=['POST'])
def add_product():
    data = request.get_json()
    TypeNews_Name = data.get('TypeNews_Name')
    check_name = db.session.query(typenews.TypeNews_Name).filter_by(TypeNews_Name=TypeNews_Name).first() is None

    if check_name:
    
        print('check_name:',check_name)
        new_typenews = typenews(TypeNews_Name = TypeNews_Name)
        db.session.add(new_typenews)
        db.session.commit()
        return jsonify({"data":{"TypeNews_ID":new_typenews.TypeNews_ID}}), 200  # Return with HTTP status 201 for created
    else:
        return {
                'message': "Trùng tên hoặc id",
                'status': 400,
                'Error': 'ERR',
            }, 400

@typenews_bp.route('/typenews', methods=['GET'])
def get_typeNewses():
    all_typeNewses = typenews.query.all()
    result = typenewses_schema.dump(all_typeNewses)
    return jsonify({"data":result}), 200

@typenews_bp.route('/typenews/<int:id>', methods=['GET'])
def get_typenews(id):
    check = db.session.query(typenews.TypeNews_ID).filter_by(TypeNews_ID=id).first() is not None
    if check:
        TypeNews = typenews.query.get_or_404(id)
        # return typenews_schema.jsonify(TypeNews),200
        result = typenews_schema.dump(TypeNews)
        return jsonify({"data": [result]}), 200
    else:
        return {
                'message': "KO tìm thấy bản ghi",
                'status': 400,
                'Error': 'ERR',
            }, 400
    
@typenews_bp.route('/typenews/<int:id>', methods=['PUT'])
def update_typenews(id):
    check = db.session.query(typenews.TypeNews_ID).filter_by(TypeNews_ID=id).first() is not None
    if check:
        TypeNews = typenews.query.get_or_404(id)
        data = request.get_json()
        check_name = db.session.query(typenews.TypeNews_Name).filter_by(TypeNews_Name=data.get('TypeNews_Name')).first() is None
        if  check_name:
            TypeNews.TypeNews_ID = data.get('TypeNews_ID')
            TypeNews.TypeNews_Name= data.get('TypeNews_Name')
            db.session.commit()
            return typenews_schema.jsonify(TypeNews),200
        else:
            return {
                'message': "Trùng tên TypeProduct",
                'status': 400,
                'Error': 'ERR',
            }, 400

    else:
        return {
                'message': "KO tìm thấy bản ghi",
                'status': 400,
                'Error': 'ERR',
            }, 400

@typenews_bp.route('/typenews/<int:id>', methods=['DELETE'])
def delete_typenews(id):
    check = db.session.query(typenews.TypeNews_ID).filter_by(TypeNews_ID=id).first() is not None
    if check:
        product = typenews.query.get_or_404(id)
        db.session.delete(product)
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
from flask import Blueprint, jsonify, request
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity, get_jwt
import jwt
from passlib.hash import pbkdf2_sha256
from app.models import User, TokenBlocklist
from app.schemas import UserSchema
from app import db
from datetime import datetime, timedelta, timezone


#Bước 3
auth_bp = Blueprint('auth_bp', __name__)

user_schema = UserSchema()
users_schema = UserSchema(many=True)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()   
    username = data.get('User_Name') 
    password = data.get('User_Password')
    email = data.get('User_Name')
    address = data.get('User_Address')
    phoneNumber = data.get('User_PhoneNumber')
    role = data.get('role', 'User')  # Mặc định là role 'user' nếu không được chỉ định

    if not username or not password:
        return jsonify(message="Missing username or password"), 400

    if User.query.filter_by(User_Name=username).first():
        return jsonify(message="Username already exists"), 400

    hashed_password = pbkdf2_sha256.hash(password)

    new_user = User(User_Name=username, User_Password=hashed_password, role=role
                    , User_Email=email, User_Address=address, User_PhoneNumber=phoneNumber)
    db.session.add(new_user)
    db.session.commit()

    return user_schema.jsonify(new_user), 201

@auth_bp.route('/getAll', methods=['GET'])
def get_users():
    try:
        all_user = User.query.all()
        result = users_schema.dump(all_user)
        return jsonify(result), 200
    except:
        return {
            'Error': 'ERR',
        },404

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('User_Name')
    password = data.get('User_Password')

    # Fetch the user from the database
    user = User.query.filter_by(User_Name=username).first()

    # Ensure the user exists and the password is correct
    if not user or not pbkdf2_sha256.verify(password, user.User_Password):
        return jsonify(message="Invalid username or password"), 401

    # Create access token
    access_token = create_access_token(identity=username)
    return jsonify(data=access_token), 200

# Route đăng xuất
@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def modify_token():
    jti = get_jwt()["jti"]
    now = datetime.now(timezone.utc)
    db.session.add(TokenBlocklist(jti=jti, created_at=now))
    db.session.commit()
    return jsonify(msg="JWT revoked")

# Bảo vệ các route sử dụng decorator @jwt_required() và kiểm tra vai trò của người dùng
@auth_bp.route('/user', methods=['GET'])
@jwt_required()
def get_user_profile():
    current_user = get_jwt_identity()
    user = User.query.filter_by(User_Name=current_user).first()
        
    if not user:
        return jsonify(message="User not found"), 404
    
    user_data = {
        'User_ID': user.User_ID,
        'User_Name': user.User_Name,
        'User_Password': user.User_Password,
        'User_Email': user.User_Email,
        'User_Address': user.User_Address,
        'User_PhoneNumber': user.User_PhoneNumber,
        'role': user.role
    }

    return jsonify({'data': user_data}), 200
# Bảo vệ các route sử dụng decorator @jwt_required() và kiểm tra vai trò của người dùng
@auth_bp.route('/admin_only', methods=['GET'])
@jwt_required()
def admin_only():
    current_user = get_jwt_identity()
    user = User.query.filter_by(User_Name=current_user).first()
    if not user or user.role != 'admin':
        return jsonify({'data':{'message':"Unauthorized", 'admin':False}}), 403

    return jsonify({'data':{'message':"Hello admin!", 'admin':True}}), 200
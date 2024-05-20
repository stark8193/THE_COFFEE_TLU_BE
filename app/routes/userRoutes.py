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
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    address = data.get('address')
    phoneNumber = data.get('phoneNumber')
    role = data.get('role', 'user')  # Mặc định là role 'user' nếu không được chỉ định

    if not username or not password:
        return jsonify(message="Missing username or password"), 400

    if User.query.filter_by(username=username).first():
        return jsonify(message="Username already exists"), 400

    hashed_password = pbkdf2_sha256.hash(password)

    new_user = User(username=username, password=hashed_password, role=role, email=email, address=address, phoneNumber=phoneNumber)
    db.session.add(new_user)
    db.session.commit()

    return user_schema.jsonify(new_user), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()

    if not user or not pbkdf2_sha256.verify(password, user.password):
        return jsonify(message="Invalid username or password"), 401

    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token), 200

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
    user = User.query.filter_by(username=current_user).first()
    if not user:
        return jsonify(message="User not found"), 404

    return user_schema.jsonify(user), 200

# Bảo vệ các route sử dụng decorator @jwt_required() và kiểm tra vai trò của người dùng
@auth_bp.route('/admin_only', methods=['GET'])
@jwt_required()
def admin_only():
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).first()
    if not user or user.role != 'admin':
        return jsonify(message="Unauthorized"), 403

    return jsonify(message="Hello admin!"), 200
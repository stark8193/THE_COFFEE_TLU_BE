from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from datetime import timedelta
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity, get_jwt
from flask_cors import CORS
import os

# Cấu hình thời gian hết hạn của JWT
ACCESS_EXPIRES = timedelta(hours=24)
UPLOAD_FOLDER = 'D:/flask/uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app = Flask(__name__)
CORS(app)

# Cấu hình cho Flask
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://u6wubyjmpuwxjtxy:4aEirCKkYb5RiSkH3vvq@b4atx5d13zgsvnoce0cy-mysql.services.clever-cloud.com/b4atx5d13zgsvnoce0cy'
app.config['JWT_SECRET_KEY'] = 'fgsdf4gdfg'
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = ACCESS_EXPIRES
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'fgsdf4gdfg'

# Khởi tạo các thành phần của Flask
db = SQLAlchemy(app)
ma = Marshmallow(app)
jwt = JWTManager(app)

# Import các Blueprint
from app.routes.menuRoutes import menu_bp 
from app.routes.typeProductRoutes import typeProduct_bp
from app.routes.userRoutes import auth_bp
from app.routes.productRoutes import product_bp
from app.routes.toppingRoutes import topping_bp 
from app.routes.product_toppingRoutes import product_topping_bp 
from app.routes.orderRoutes import order_bp 
from app.routes.uploadRoutes import upload_bp
from app.routes.typeNewsRoutes import typenews_bp
from app.routes.newsRoute import news_bp

# Đăng ký các Blueprint
app.register_blueprint(product_bp, url_prefix='/api')
app.register_blueprint(topping_bp, url_prefix='/api')
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(menu_bp, url_prefix='/api')
app.register_blueprint(typeProduct_bp, url_prefix='/api')
app.register_blueprint(upload_bp)
app.register_blueprint( product_topping_bp , url_prefix='/api')
app.register_blueprint(typenews_bp, url_prefix='/api') 
app.register_blueprint(news_bp, url_prefix='/api')  
app.register_blueprint(order_bp, url_prefix='/api') 

from app import routes  
from app.models import TokenBlocklist

@app.route("/")
def helloWorld():
    return "Xin chào, thế giới cross-origin!"

# Hàm callback để kiểm tra nếu một JWT tồn tại trong danh sách blocklist
@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload: dict) -> bool:
    jti = jwt_payload["jti"]
    token = db.session.query(TokenBlocklist.id).filter_by(jti=jti).scalar()
    return token is not None



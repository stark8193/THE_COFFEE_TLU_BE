from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from datetime import timedelta
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity, get_jwt

ACCESS_EXPIRES = timedelta(hours=1)
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://u6wubyjmpuwxjtxy:4aEirCKkYb5RiSkH3vvq@b4atx5d13zgsvnoce0cy-mysql.services.clever-cloud.com/b4atx5d13zgsvnoce0cy'
app.config['JWT_SECRET_KEY'] = 'fgsdf4gdfg'
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = ACCESS_EXPIRES
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'fgsdf4gdfg'
db = SQLAlchemy(app)
ma = Marshmallow(app)


# Khởi tạo JWTManager
jwt = JWTManager(app)



# Thiết lập JWT với ứng dụng Flask
def configure_jwt(app):
    jwt.init_app(app)
    
# Thêm middleware JWT vào ứng dụng Flask
configure_jwt(app)



# Bước 5
from app.routes.menuRoutes import menu_bp 
from app.routes.typeProductRoutes import typeProduct_bp
from app.routes.userRoutes import auth_bp
from app.routes.productRoutes import product_bp
from app.routes.toppingRoutes import topping_bp 
from app.routes.product_toppingRoutes import product_topping_bp 

app.register_blueprint(product_bp, url_prefix='/api')
app.register_blueprint(topping_bp, url_prefix='/api')
app.register_blueprint(auth_bp, url_prefix='/api/auth') # Import the blueprint  
app.register_blueprint(menu_bp, url_prefix='/api')
app.register_blueprint(typeProduct_bp, url_prefix='/api')

app.register_blueprint( product_topping_bp , url_prefix='/api')

from app.routes.typeNewsRoutes import typenews_bp  # Import the blueprint
app.register_blueprint(typenews_bp, url_prefix='/api')  # Optionally specify a URL prefix

from app.routes.newsRoute import news_bp  # Import the blueprint
app.register_blueprint(news_bp, url_prefix='/api')  # Optionally specify a URL prefix

from app import routes  # Import routes after registering blueprints
from app.models import TokenBlocklist
# Callback function to check if a JWT exists in the database blocklist
@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload: dict) -> bool:
    jti = jwt_payload["jti"]
    token = db.session.query(TokenBlocklist.id).filter_by(jti=jti).scalar()

    return token is not None


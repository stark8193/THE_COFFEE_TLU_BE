from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://ulkmhktxc7ei03sm:54nBAvixeXNrcelrpIjQ@beoza5v9jn88nqcpay9b-mysql.services.clever-cloud.com/beoza5v9jn88nqcpay9b'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)
# Bước 5
from app.routes.menuRoutes import menu_bp
from app.routes.typeProductRoutes import typeProduct_bp
from app.routes.productRoutes import product_bp  # Import the blueprint

app.register_blueprint(menu_bp, url_prefix='/api')
app.register_blueprint(typeProduct_bp, url_prefix='/api')
app.register_blueprint(product_bp, url_prefix='/api')  # Optionally specify a URL prefix




from app import routes  # Import routes after registering blueprints


from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://udsbjqd3tgmnylgf:JWkkGksQRgblts5PVSFL@bzfb6kzzfovy92oo6q8z-mysql.services.clever-cloud.com/bzfb6kzzfovy92oo6q8z'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)
# Bước 5
from app.routes.productRoutes import product_bp  # Import the blueprint
app.register_blueprint(product_bp, url_prefix='/api')  # Optionally specify a URL prefix




from app import routes  # Import routes after registering blueprints


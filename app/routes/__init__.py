from flask import Blueprint

menu_bp = Blueprint('menus', __name__)
typeProduct_bp = Blueprint('typeProducts', __name__)
product_bp = Blueprint('products', __name__)
#Bước 4

from app.routes import productRoutes  # Import routes module
from app.routes import menuRoutes
from app.routes import typeProductRoutes
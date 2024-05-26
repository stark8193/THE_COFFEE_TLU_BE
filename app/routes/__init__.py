from flask import Blueprint

menu_bp = Blueprint('menus', __name__)
typeProduct_bp = Blueprint('typeproducts', __name__)
product_bp = Blueprint('products', __name__)
topping_bp = Blueprint('topppings', __name__)
auth_bp = Blueprint('auths', __name__)
product_topping_bp = Blueprint('product_toppings', __name__)
upload_bp = Blueprint('upload_bp', __name__)
order_bp = Blueprint('orders', __name__)

#Bước 4

from app.routes import *  # Import routes module

# from app.routes import productRoutes, userRoutes  # Import routes module

from flask import Blueprint

product_bp = Blueprint('products', __name__)
#Bước 4

from app.routes import productRoutes  # Import routes module

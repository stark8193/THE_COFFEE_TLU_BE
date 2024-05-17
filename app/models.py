from app import db
import datetime

# Bước 1: Định nghĩa model Menu
class Menu(db.Model):
    __tablename__ = 'Menu'  # Xác định tên bảng một cách rõ ràng
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    type_products = db.relationship('TypeProduct', backref='Menu', lazy=True)


# Bước 2: Định nghĩa model TypeProduct
class TypeProduct(db.Model):
    __tablename__ = 'TypeProduct'  # Xác định tên bảng một cách rõ ràng
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    image = db.Column(db.String(100), unique=True, nullable=False)
    menu_id = db.Column(db.Integer, db.ForeignKey('Menu.id'), nullable=False)
    products = db.relationship('Product', backref='TypeProduct', lazy=True)

# Bước 3: Định nghĩa model Product
class Product(db.Model):
    __tablename__ = 'Product'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    image = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.String(200))
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    type_product_id = db.Column(db.Integer, db.ForeignKey('TypeProduct.id'), nullable=False)

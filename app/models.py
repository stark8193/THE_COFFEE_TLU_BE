from app import db
import uuid
import datetime

# Bước 1: Định nghĩa model Menu
class Menu(db.Model):
    __tablename__ = 'Menu'  # Xác định tên bảng một cách rõ ràng
    Menu_ID = db.Column(db.String(100), unique=True, primary_key=True, default=lambda: str(uuid.uuid4()))
    Name_Menu = db.Column(db.Text, unique=True, nullable=False)
    type_products = db.relationship('typeproduct', backref='Menu', lazy=True)

class TokenBlocklist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), nullable=False, index=True)
    created_at = db.Column(db.DateTime, nullable=False)
class typeproduct(db.Model):
    __tablename__ = 'typeproduct'  # Xác định tên bảng một cách rõ ràng
    TypeProduct_ID = db.Column(db.String(100), unique=True, primary_key=True, default=lambda: str(uuid.uuid4()))
    TypeProduct_Name = db.Column(db.String(100), unique=True, nullable=False)
    TypeProduct_Img = db.Column(db.String(100), unique=True, nullable=False)
    Menu_ID = db.Column(db.String(100), db.ForeignKey('Menu.Menu_ID'), nullable=False)
    products = db.relationship('product', backref='typeproduct', lazy=True)

Product_Topping = db.Table(
    "Product_Topping",
    db.Column('idProduct', db.String(100), db.ForeignKey('product.idProduct'),primary_key=True),
    db.Column('Topping_ID', db.String(100), db.ForeignKey('Topping.Topping_ID'), primary_key=True)
)

class product(db.Model):
    __tablename__ = 'product'
    idProduct = db.Column(db.String(100), unique=True, primary_key=True, default=lambda: str(uuid.uuid4()))
    Product_Name = db.Column(db.String(100), unique=True, nullable=False)
    Product_Image = db.Column(db.String(100), unique=True, nullable=False)
    Product_Price = db.Column(db.Float, nullable=False)
    Product_Description = db.Column(db.String(1000))
    TypeProduct_ID = db.Column(db.String(100), db.ForeignKey('typeproduct.TypeProduct_ID'), nullable=False)
    toppings = db.relationship("Topping", secondary=Product_Topping, back_populates="products")

class Topping(db.Model):
    __tablename__ = 'Topping'  # Xác định tên bảng một cách rõ ràng
    Topping_ID = db.Column(db.String(100), unique=True, primary_key=True, default=lambda: str(uuid.uuid4()))
    Topping_Name = db.Column(db.String(100), unique=True, nullable=False)
    Topping_Price = db.Column(db.Float, nullable=False)
    products = db.relationship("product", secondary=Product_Topping, back_populates="toppings")

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.Text(), nullable=False)
    address = db.Column(db.Text(), nullable=False)
    phoneNumber = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), default='user', nullable=False) 

class typenews(db.Model):
    TypeNews_ID = db.Column(db.Integer, primary_key = True)
    TypeNews_Name = db.Column(db.String(100), nullable=False)

class news(db.Model):
    News_ID = db.Column(db.String(300), primary_key = True)
    News_Title = db.Column(db.String(100))
    News_Image = db.Column(db.String(300))
    News_Description = db.Column(db.Text)
    News_Content = db.Column(db.Text)
    News_Time = db.Column(db.String(100), default='default_time_value')
    TypeNews_ID = db.Column(db.String(300), db.ForeignKey('typenews.TypeNews_ID'), nullable=False)








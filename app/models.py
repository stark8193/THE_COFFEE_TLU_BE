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
    products = db.relationship('product', backref=db.backref('typeproduct', lazy=True), overlaps="products,typeproduct")

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
    order_details = db.relationship('Order_Detail', backref='product', lazy=True)
    type_product = db.relationship('typeproduct', backref=db.backref('product', lazy=True),overlaps="products,typeproduct")

class Topping(db.Model):
    __tablename__ = 'Topping'  # Xác định tên bảng một cách rõ ràng
    Topping_ID = db.Column(db.String(100), unique=True, primary_key=True, default=lambda: str(uuid.uuid4()))
    Topping_Name = db.Column(db.String(100), unique=True, nullable=False)
    Topping_Price = db.Column(db.Float, nullable=False)
    products = db.relationship("product", secondary=Product_Topping, back_populates="toppings")


class User(db.Model): 
    __tablename__ = 'User'
    User_ID = db.Column(db.String(100), unique=True, primary_key=True, default=lambda: str(uuid.uuid4()))
    User_Name = db.Column(db.String(100), unique=True, nullable=False)
    User_Password = db.Column(db.String(100), nullable=False)
    User_Email = db.Column(db.Text(), nullable=False) 
    User_Address = db.Column(db.Text(), nullable=False)
    User_PhoneNumber = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), default='User', nullable=False) 
    users = db.relationship('Order', backref='User', lazy=True)

class Order(db.Model):
    __tablename__ = 'Order'
    Order_ID = db.Column(db.String(100), unique=True, primary_key=True, default=lambda: str(uuid.uuid4()))
    Order_Date = db.Column(db.DateTime, default= datetime.datetime.utcnow)
    Order_Status = db.Column(db.String(100), nullable=False)
    User_ID = db.Column(db.String(100), db.ForeignKey('User.User_ID'), nullable=False)
    order_details = db.relationship('Order_Detail', backref='Order', lazy=True)

class Order_Detail(db.Model):
    __tablename__ = 'Order_Detail'
    Order_Detail_ID = db.Column(db.String(100), unique=True, primary_key=True, default=lambda: str(uuid.uuid4()))
    Order_Quantity = db.Column(db.Integer, nullable=False)
    Order_Size = db.Column(db.String(100), nullable=False)
    Order_ID = db.Column(db.String(100), db.ForeignKey('Order.Order_ID'), nullable=False)
    idProduct = db.Column(db.String(100), db.ForeignKey('product.idProduct'), nullable=False)
    topping_additions = db.relationship('Topping_Addition', backref='Order_Detail', lazy=True)

class Topping_Addition(db.Model):
    __tablename__ = 'Topping_Addition'
    Topping_Addition_ID = db.Column(db.String(100), unique=True, primary_key=True, default=lambda: str(uuid.uuid4()))
    Topping_Addition_Name = db.Column(db.String(100),unique=True)
    Topping_Addition_Price = db.Column(db.Integer)
    Order_Detail_ID = db.Column(db.String(100), db.ForeignKey('Order_Detail.Order_Detail_ID'), nullable=False)
    
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
    type_news = db.relationship('typenews', backref=db.backref('news', lazy=True))








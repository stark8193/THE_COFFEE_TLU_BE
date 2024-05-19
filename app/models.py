from app import db


# Bước 1
class TokenBlocklist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), nullable=False, index=True)
    created_at = db.Column(db.DateTime, nullable=False)
class Product1(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.String(200))
    price = db.Column(db.Float)
    qty = db.Column(db.Integer)

    def __init__(self, name, description, price, qty):
        self.name = name
        self.description = description
        self.price = price
        self.qty = qty

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








from app import ma
from app.models import *


# Bước 2
class MenuSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Menu

class TypeProductSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = typeproduct

class ProductSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model= product
    TypeProduct_ID = ma.auto_field()

class ToppingSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model= Topping

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User

class TypeNewsSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model= typenews
class NewsSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = news
    TypeNews_ID = ma.auto_field()

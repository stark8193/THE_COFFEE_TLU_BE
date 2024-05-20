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

class ToppingSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model= Topping



class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User


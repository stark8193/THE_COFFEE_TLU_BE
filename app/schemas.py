from app import ma
from app.models import *


# Bước 2
class MenuSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Menu

class TypeProductSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = TypeProduct

class ProductSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model= Product



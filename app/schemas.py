from app import ma
from app.models import Product


# Bước 2
class ProductSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Product

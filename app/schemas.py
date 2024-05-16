from app import ma
from app.models import Product1, User


# Bước 2
class ProductSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Product1
class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User

from app import ma
from app.models import Product1, User, typenews, news


# Bước 2
class ProductSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Product1
class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
class TypeNewsSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model= typenews
class NewsSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = news

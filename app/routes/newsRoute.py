from flask import Blueprint, jsonify, request
from app.models import news,typenews
from app.schemas import NewsSchema
from app import db

news_bp = Blueprint('news_bp', __name__)

news_schema = NewsSchema()
newses_schema = NewsSchema(many=True)

@news_bp.route('/news', methods=['POST'])
def add_news():
    data = request.get_json()
    id = data.get("News_ID")
    title = data.get('News_Title')
    image = data.get('News_Image')
    description = data.get('News_Description')
    content = data.get('News_Content')
    time = data.get('News_Time')
    typenews_id = data.get('TypeNews_ID')

    check_typenews_id = db.session.query(typenews.TypeNews_ID).filter_by(TypeNews_ID=typenews_id).first() is not None
    check_title = db.session.query(news.News_Title).filter_by(News_Title = title).first() is None
    check_image = db.session.query(news.News_Image).filter_by(News_Image = image).first() is None

    if check_typenews_id and check_title and check_image:

        new_news = news(News_ID = id ,News_Title=title, News_Image=image, News_Description = description, News_Content = content , News_Time=time, TypeNews_ID=typenews_id)
        db.session.add(new_news)
        db.session.commit()
        return news_schema.jsonify(new_news), 200  # Return with HTTP status 201 for created
    else:
        return {
                'message': "Trùng tên hoặc link ảnh, hoặc ko tồn tại trong TypeProduct",
                'status': 400,
                'Error': 'ERR',
            }, 400

@news_bp.route('/news', methods=['GET'])
def get_newses():
    all_newses = news.query.all()
    result = newses_schema.dump(all_newses)
    return jsonify(result), 200

@news_bp.route('/news/<string:id>', methods=['GET'])
def get_news(id):
    check = db.session.query(news.News_ID).filter_by(News_ID=id).first() is not None
    if check:
        News = news.query.get_or_404(id)
        return news_schema.jsonify(News),200
    else:
        return {
                'message': "KO tìm thấy bản ghi",
                'status': 400,
                'Error': 'ERR',
            }, 400
    
@news_bp.route('/news/<string:id>', methods=['PUT'])
def update_news(id):
    check = db.session.query(news.News_ID).filter_by(News_ID=id).first() is not None
    if check:
        News = news.query.get_or_404(id)
        data = request.get_json()
        check_typenews_id = db.session.query(typenews.TypeNews_ID).filter_by(TypeNews_ID=data.get('TypeNews_ID')).first() is not None
        check_title = db.session.query(news.News_Title).filter_by(News_Title=data.get('News_Title')).first() is None
        check_image = db.session.query(news.News_Image).filter_by(News_Image=data.get('News_Image')).first() is None
        if check_title and check_image and check_typenews_id:
            News.News_ID = data.get("News_ID")
            News.News_Title= data.get('News_Title')
            News.News_Image = data.get('News_Image')
            News.News_Description= data.get('News_Description')
            News.News_Content = data.get('News_Content')
            News.News_Time  = data.get('News_Time')
            News.TypeNews_ID = data.get('TypeNews_ID')
            db.session.commit()
            return news_schema.jsonify(News),200
        else:
            return {
                'message': "Trùng tên hoặc link ảnh, hoặc ko tồn tại trong TypeProduct",
                'status': 400,
                'Error': 'ERR',
            }, 400

    else:
        return {
                'message': "KO tìm thấy bản ghi",
                'status': 400,
                'Error': 'ERR',
            }, 400

@news_bp.route('/news/<string:id>', methods=['DELETE'])
def delete_news(id):
    check = db.session.query(news.News_ID).filter_by(News_ID=id).first() is not None
    if check:
        print('check:',check)
        News = news.query.get_or_404(id)
        db.session.delete(News)
        db.session.commit()
        return{
                'message': 'Da xoa ban ghi',
                'status': 200,
            }, 200  # Return with HTTP status 204 for no content
    else:
        return {
                'message': "KO tim thay ban ghi",
                'status': 400,
                'Error': 'ERR',
            }, 400
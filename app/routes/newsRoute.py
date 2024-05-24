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
    try:
        news_with_type = db.session.query(news, typenews).join(typenews).all()
        result = []
        for newsItem, typenewsItem in news_with_type:
            news_data = {
                'News_ID': newsItem.News_ID,
                'News_Title': newsItem.News_Title,
                'News_Image': newsItem.News_Image,
                'News_Description': newsItem.News_Description,
                'News_Content': newsItem.News_Content,
                'News_Time': newsItem.News_Time,
                'TypeNews_ID': typenewsItem.TypeNews_ID,
                'TypeNews_Name': typenewsItem.TypeNews_Name
            }
            result.append(news_data)
        return jsonify({"data":result}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500


@news_bp.route('/news/<string:id>', methods=['GET'])
def get_news(id):
    check = db.session.query(news.News_ID).filter_by(News_ID=id).first() is not None
    if check:
        News = news.query.get_or_404(id)
        result = news_schema.dump(News)
        return jsonify({"data":result}), 200
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
@news_bp.route('/news/pagination/data', methods=['GET'])
def pagination():
    page = int(request.args.get('page', 1))
    pageSize = int(request.args.get('pageSize', 10))
    typeNews = request.args.get('typeNews')

    offset = (page - 1) * pageSize

    # Perform query to get paginated data
    news_data = db.session.query(news, typenews.TypeNews_Name).\
                join(typenews, news.TypeNews_ID == typenews.TypeNews_ID).\
                filter(typenews.TypeNews_Name == typeNews).\
                limit(pageSize).offset(offset).all()

    total_count = db.session.query(news).\
                join(typenews, news.TypeNews_ID == typenews.TypeNews_ID).\
                filter(typenews.TypeNews_Name == typeNews).\
                count()

    return jsonify({
        'data': [serialize_data(n, t) for n, t in news_data],
        'total_count': total_count
    })

def serialize_data(news_obj, type_name):
    return {
        'News_ID': news_obj.News_ID,
        'News_Title': news_obj.News_Title,
        'News_Image': news_obj.News_Image,
        'News_Description': news_obj.News_Description,
        'News_Content': news_obj.News_Content,
        'News_Time': news_obj.News_Time,
        'TypeNews_Name': type_name
    }

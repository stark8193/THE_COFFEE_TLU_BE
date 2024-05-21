from flask import Flask, render_template, request, Blueprint, url_for
import requests
upload_bp = Blueprint('upload_bp', __name__)

@upload_bp.route('/')
def upload_form():
    return render_template('upload.html')

@upload_bp.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        # Kiểm tra xem tệp đã được chọn hay chưa
        if 'image' not in request.files:
            return 'No file part'
        
        file = request.files['image']
        
        # Kiểm tra xem tên tệp có tồn tại hay không
        if file.filename == '':
            return 'No selected file'
        
        # Gửi hình ảnh đến ChatGPT API
        url = "ChatGPT_API_URL"
        files = {'image': file.read()}
        response = requests.post(url, files=files)

        # Xử lý kết quả từ API
        if response.status_code == 200:
            return response.text
        else:
            return 'Error: ' + str(response.status_code)

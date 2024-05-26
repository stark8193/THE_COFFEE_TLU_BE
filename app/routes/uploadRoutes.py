from flask import Blueprint, request, send_from_directory, jsonify
import os
from app import app

upload_bp = Blueprint('upload_bp', __name__)

@upload_bp.route('/uploads/<filename>', methods=['GET'])
def uploaded_file(filename):
    try:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if not os.path.exists(file_path):
            return jsonify({'error': 'Không tìm thấy file'}), 404
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@upload_bp.route('/uploads', methods=['POST'])
def upload_file():
    if 'image' not in request.files:
        return jsonify({'error': 'Không có phần file'}), 400

    file = request.files['image']
    print(file)
    if file.filename == '':
        return jsonify({'error': 'Không có file nào được chọn'}), 400

    try:
        filename = file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return jsonify({'message': 'Tải file lên thành công', 'filename': filename}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

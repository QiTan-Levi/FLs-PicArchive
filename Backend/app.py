import json
from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
import time
import uuid
import random
import os
from werkzeug.utils import secure_filename
from utils import (
    init_db_connections,
    send_verification_email,
    verification_codes,
)
import mimetypes
from datetime import datetime, timedelta

app = Flask(__name__)
CORS(app, supports_credentials=True, resources={
    r"/*": {
        "origins": ["http://localhost:5173", "http://localhost:5000"],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"],
        "expose_headers": ["Content-Range", "X-Content-Range"],
        "supports_credentials": True
    }
})

# 初始化数据库连接
mysql = init_db_connections()

# 配置上传文件存储路径
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'svg'}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    return "This is backend of Focus's Transportation Archive.\nPerhaps, you should use the frontend to visit the website."

@app.route('/api/images', methods=['GET'])
def get_images():
    category = request.args.get('category', '全部')
    search_query = request.args.get('search', '')
    
    cursor = mysql.cursor()
    base_query = """
        SELECT i.id, i.file_type, i.aircraft_model, i.shooting_location, 
               i.image_description, i.upload_time, i.is_featured, i.user_id, 
               u.username
        FROM images i
        JOIN users u ON i.user_id = u.id
        WHERE i.is_pending = 0
    """
    
    if category == '全部':
        if search_query:
            cursor.execute(base_query + " AND (i.aircraft_model LIKE %s OR i.image_description LIKE %s)", 
                         (f'%{search_query}%', f'%{search_query}%'))
        else:
            cursor.execute(base_query)
    else:
        if search_query:
            cursor.execute(base_query + " AND i.aircraft_model = %s AND (i.aircraft_model LIKE %s OR i.image_description LIKE %s)", 
                         (category, f'%{search_query}%', f'%{search_query}%'))
        else:
            cursor.execute(base_query + " AND i.aircraft_model = %s", (category,))
    
    images = cursor.fetchall()
    result = []
    
    for image in images:
        result.append({
            'id': image[0],
            'aircraft_model': image[2],
            'location': image[3],
            'description': image[4],
            'upload_time': image[5].strftime('%Y-%m-%d %H:%M:%S') if image[5] else None,
            'user_id': image[7],
            'username': image[8],
            'avatar': image[9],
            'filename': image[1],
            'content_type': 'image/jpeg'  # 假设所有图片都是jpeg格式
        })
    
    return jsonify({
        'status': 'success',
        'data': result
    })



@app.route('/api/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return jsonify({'status': 'failed', 'message': '没有文件被上传'})
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'status': 'failed', 'message': '没有选择文件'})
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        content_type = mimetypes.guess_type(filename)[0]
        
        # 使用文件名作为文件ID
        file_id = filename
        # 获取表单数据
        aircraft_model = request.form.get('aircraft_model', '')
        location = request.form.get('location', '')
        description = request.form.get('description', '')
        user_id = request.form.get('user_id')
        # 插入MySQL记录
        cursor = mysql.cursor()
        cursor.execute("""
            INSERT INTO images (user_id, file_id, aircraft_model, location, 
                              description, upload_time, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (user_id, str(file_id), aircraft_model, location, 
              description, datetime.now(), 0))
        mysql.commit()
        return jsonify({'status': 'success', 'message': '图片上传成功'})
    return jsonify({'status': 'failed', 'message': '不支持的文件类型'})

@app.route('/api/batch-upload', methods=['POST'])
def batch_upload_images():
    files = request.files.getlist('files')
    if not files:
        return jsonify({'status': 'failed', 'message': '没有文件被上传'})

    user_id = request.form.get('user_id')
    images_data = []
    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_id = filename
            aircraft_model = request.form.get('aircraft_model', '')
            location = request.form.get('location', '')
            description = request.form.get('description', '')
            images_data.append((user_id, str(file_id), aircraft_model, location, description, datetime.now(), 0))

    if images_data:
        cursor = mysql.cursor()
        cursor.executemany("""
            INSERT INTO images (user_id, file_id, aircraft_model, location, 
                              description, upload_time, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, images_data)
        mysql.commit()
        return jsonify({'status': 'success', 'message': '批量图片上传成功'})
    return jsonify({'status': 'failed', 'message': '不支持的文件类型'})

@app.route('/api/image/<file_id>', methods=['GET'])
def get_image(file_id):
    try:
        cursor = mysql.cursor()
        cursor.execute("SELECT file_id, content_type FROM images WHERE file_id = %s", (file_id,))
        image = cursor.fetchone()
        if not image:
            return jsonify({'status': 'failed', 'message': '图片不存在'}), 404

        file_path = os.path.join(app.config['UPLOAD_FOLDER'], image[0])
        with open(file_path, 'rb') as file_obj:
            response = make_response(file_obj.read())
            response.mimetype = image[1]
            return response
    except Exception as e:
        return jsonify({'status': 'failed', 'message': '图片不存在'}), 404

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data['username']
    password = data['password']
    email = data['email']
    regis_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    
    cursor = mysql.cursor()
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    if cursor.fetchone():
        return {"status":"failed","message":"Username already exists."}
    
    # 读取 logo.svg 文件内容
    logo_path = os.path.join(os.path.dirname(__file__), 'logo.svg')
    with open(logo_path, 'r', encoding='utf-8') as f:
        logo_content = f.read()

    cursor.execute("SELECT MAX(id) FROM users")
    last_id = cursor.fetchone()[0]
    id = last_id+1 if last_id else 1
    cursor.execute("INSERT INTO users (id, username, password, email, regis_time, status) VALUES (%s, %s, %s, %s, %s, 1)", 
                  (id, username, password, email, regis_time))
    mysql.commit()
    
    return {"status": "success", "message": "注册成功"}

@app.route('/send-verification-code', methods=['POST'])
def send_verification_code():
    data = request.json
    email = data['email']
    code = str(random.randint(100000, 999999))
    verification_codes[email] = {
        'code': code,
        'expire_time': time.time() + 300
    }
    send_verification_email(email, code)
    return {"status": "success", "message": "验证码已发送"}

@app.route('/api/login', methods=['POST'])
def login():
    try:
        data = request.json
        print("接收到的登录数据:", data)  # 调试日志

        if not data:
            return {"status": "failed", "message": "未接收到登录数据"}, 400

        # 检查必要的字段是否存在
        if not any(key in data for key in ['password', 'verificationCode']):
            return {"status": "failed", "message": "请提供密码或验证码"}, 400

        if 'password' in data:
            if not data.get('username'):
                print("Password login attempt missing username. Received data:", data) # 添加调试日志
                return {"status": "failed", "message": "用户名不能为空"}, 400

            username = data['username']
            password = data['password']
            cursor = mysql.cursor()
            cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", 
                          (username, password))
            user = cursor.fetchone()
            if not user:
                return {"status": "failed", "message": "用户名或密码错误"}, 401

            # 生成响应
            response = make_response({
                "status": "success", 
                "message": "登录成功",
                "data": {
                    "userId": user[0],
                    "username": user[1],
                    "userAvatar": user[3]  # 从数据库中获取头像信息
                }
            })

            # 设置 cookie
            user_info = {
                "userId": user[0],
                "username": user[1],
                "userAvatar": user[3]  # 添加 userAvatar
            }
            encoded_user_info = json.dumps(user_info)
            response.set_cookie('user-info', encoded_user_info, max_age=3600*24, path='/', httponly=False, samesite='Lax')
            response.set_cookie('token', str(uuid.uuid4()), max_age=3600*24, path='/', httponly=True, samesite='Lax')

            #记录最后登录时间
            cursor.execute("UPDATE users SET last_login = %s WHERE id = %s", (datetime.now(), user[0]))
            mysql.commit()

            return response

        elif 'verificationCode' in data:
            if not data.get('email'):
                return {"status": "failed", "message": "邮箱不能为空"}, 400

            email = data['email']
            code = data['verificationCode']

            if email not in verification_codes:
                return {"status": "failed", "message": "请先获取验证码"}, 401
            if time.time() > verification_codes[email]['expire_time']:
                return {"status": "failed", "message": "验证码已过期"}, 401
            if code != verification_codes[email]['code']:
                return {"status": "failed", "message": "验证码错误"}, 401

            del verification_codes[email]
            cursor = mysql.cursor()
            cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
            user = cursor.fetchone()
            if not user:
                return {"status": "failed", "message": "该邮箱未注册"}, 401

            # 生成token并设置cookie
            token = str(uuid.uuid4())
            user_info = {
                "userId": user[0],
                "username": user[1],
                "userAvatar": user[3]  # 从数据库中获取头像信息
            }
            response = make_response({
                "status": "success", 
                "message": "登录成功",
                "data": {
                    "userId": user[0],
                    "username": user[1],
                    "userAvatar": user_info["userAvatar"]
                }
            })
            encoded_user_info = json.dumps(user_info)
            response.set_cookie('user-info', encoded_user_info, max_age=3600*24, path='/', httponly=False, samesite='Lax')
            response.set_cookie('token', token, max_age=3600*24, path='/', httponly=True, samesite='Lax') # 建议 token 设置 httponly
            return response

        else:
            return {"status": "failed", "message": "无效的登录请求格式"}, 400

    except Exception as e:
        print("登录错误:", str(e))  # 错误日志
        return {"status": "failed", "message": f"登录失败: {str(e)}"}, 500

@app.route('/api/upload_avatar', methods=['POST'])
def upload_avatar():
    if 'file' not in request.files:
        return jsonify({'status': 'failed', 'message': '没有文件被上传'})
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'status': 'failed', 'message': '没有选择文件'})
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        avatar_url = url_for('uploaded_file', filename=filename)
        user_id = request.form.get('user_id')
        cursor = mysql.cursor()
        cursor.execute("""
            UPDATE users SET avatar_url = %s WHERE id = %s
        """, (avatar_url, user_id))
        mysql.commit()
        return jsonify({'status': 'success', 'message': '头像上传成功', 'avatar_url': avatar_url})
    return jsonify({'status': 'failed', 'message': '不支持的文件类型'})

@app.route('/uploads')
def uploaded_file():
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)



@app.route('/api/featured-images', methods=['GET'])
def get_featured_images():
    cursor = mysql.cursor()
    three_days_ago = datetime.now() - timedelta(days=3)
    cursor.execute('''
        SELECT i.id, i.aircraft_model, i.image_description, 
               i.upload_time, i.user_id, u.username, COUNT(c.id) as likes_count
        FROM images i
        JOIN users u ON i.user_id = u.id
        LEFT JOIN comments c ON i.id = c.image_id AND c.type = 1
        WHERE i.upload_time >= %s
        GROUP BY i.id, i.aircraft_model, i.image_description, i.upload_time, i.user_id, u.username
        ORDER BY likes_count DESC, i.upload_time DESC
        LIMIT 10
    ''', (three_days_ago,))
    images = cursor.fetchall()
    result = []
    for image in images:
        result.append({
            'id': image[0],
            'aircraft_model': image[1],
            'description': image[2],
            'upload_time': image[3].strftime('%Y-%m-%d %H:%M:%S') if image[3] else None,
            'user_id': image[4],
            'username': image[5],
            'content_type': 'image/jpeg'
        })
    return jsonify({'status': 'success', 'data': result})

if __name__ == '__main__':
    app.run(debug=True)
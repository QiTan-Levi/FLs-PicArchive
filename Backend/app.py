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
from bson.objectid import ObjectId
from datetime import datetime

app = Flask(__name__)
CORS(app, supports_credentials=True, resources={
    r"/*": {
        "origins": ["http://localhost:5173"],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"],
        "expose_headers": ["Content-Range", "X-Content-Range"],
        "supports_credentials": True
    }
})

# 初始化数据库连接
mysql, mongodb, fs = init_db_connections()

# 配置上传文件存储路径
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

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
        SELECT i.id, i.file_id, i.aircraft_model, i.location, 
               i.description, i.upload_time, i.status, i.user_id, 
               u.username
        FROM images i
        JOIN users u ON i.user_id = u.id
        WHERE i.status = 1
    """
    
    if category == '全部':
        if search_query:
            cursor.execute(base_query + " AND (i.aircraft_model LIKE %s OR i.description LIKE %s)", 
                         (f'%{search_query}%', f'%{search_query}%'))
        else:
            cursor.execute(base_query)
    else:
        if search_query:
            cursor.execute(base_query + " AND i.aircraft_model = %s AND (i.aircraft_model LIKE %s OR i.description LIKE %s)", 
                         (category, f'%{search_query}%', f'%{search_query}%'))
        else:
            cursor.execute(base_query + " AND i.aircraft_model = %s", (category,))
    
    images = cursor.fetchall()
    result = []
    
    for image in images:
        file_obj = fs.get(ObjectId(image[1]))
        result.append({
            'id': image[0],
            'aircraft_model': image[2],
            'location': image[3],
            'description': image[4],
            'upload_time': image[5].strftime('%Y-%m-%d %H:%M:%S') if image[5] else None,
            'user_id': image[7],
            'username': image[8],
            'filename': file_obj.filename,
            'content_type': file_obj.content_type
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
        
        # 存储文件到MongoDB
        file_id = fs.put(
            file,
            filename=filename,
            content_type=content_type,
            metadata={
                'fileType': 'image',
                'originalName': filename,
                'uploadTime': datetime.now()
            }
        )
        
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

@app.route('/api/image/<file_id>', methods=['GET'])
def get_image(file_id):
    try:
        file_obj = fs.get(ObjectId(file_id))
        response = make_response(file_obj.read())
        response.mimetype = file_obj.content_type
        return response
    except Exception as e:
        return jsonify({'status': 'failed', 'message': '图片不存在'}), 404

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data['username']
    password = data['password']
    email = data['email']
    RegisTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    
    cursor = mysql.cursor()
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    if cursor.fetchone():
        return {"status":"failed","message":"Username already exists."}
    
    # 读取 logo.svg 文件内容
    logo_path = os.path.join(os.path.dirname(__file__), 'logo.svg')
    with open(logo_path, 'r', encoding='utf-8') as f:
        logo_content = f.read()
    
    userA = {
        "username": data['username'],
        "avatar": logo_content
    }
    mongodb.users.insert_one(userA)

    cursor.execute("SELECT MAX(id) FROM users")
    last_id = cursor.fetchone()[0]
    id = last_id+1 if last_id else 1
    cursor.execute("INSERT INTO users (id, username, password, email, RegisTime, status) VALUES (%s, %s, %s, %s, %s, 1)", 
                  (id, username, password, email, RegisTime))
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

            # 从 MongoDB 获取用户头像
            userA = mongodb.users.find_one({"username": username})
            
            # 生成响应
            response = make_response({
                "status": "success", 
                "message": "登录成功",
                "data": {
                    "userId": user[0],
                    "username": user[1],
                    "userAvatar": f"/api/avatar/{user[0]}"
                }
            })
            
            # 设置 cookie
            user_info = {
                "userId": user[0],
                "username": user[1],
                "userAvatar": f"/api/avatar/{user[0]}"  # 添加 userAvatar
            }
            # 使用 encodeURIComponent 对 JSON 字符串进行编码，防止特殊字符问题
            encoded_user_info = json.dumps(user_info)
            response.set_cookie('user-info', encoded_user_info, max_age=3600*24, path='/', httponly=False, samesite='Lax')
            response.set_cookie('token', str(uuid.uuid4()), max_age=3600*24, path='/', httponly=True, samesite='Lax') # 建议 token 设置 httponly
            
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
            userA = mongodb.users.find_one({"username": user[1]})
            user_info = {
                "userId": user[0],
                "username": user[1],
                "userAvatar": f"/api/avatar/{user[0]}" # 添加 userAvatar
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
            # 使用 encodeURIComponent 对 JSON 字符串进行编码，防止特殊字符问题
            encoded_user_info = json.dumps(user_info)
            response.set_cookie('user-info', encoded_user_info, max_age=3600*24, path='/', httponly=False, samesite='Lax')
            response.set_cookie('token', token, max_age=3600*24, path='/', httponly=True, samesite='Lax') # 建议 token 设置 httponly
            return response

        else:
            return {"status": "failed", "message": "无效的登录请求格式"}, 400

    except Exception as e:
        print("登录错误:", str(e))  # 错误日志
        return {"status": "failed", "message": f"登录失败: {str(e)}"}, 500





@app.route('/api/avatar/<user_id>', methods=['GET'])
def get_avatar(user_id):
    try:
        userA = mongodb.users.find_one({"username": user_id})
        if userA and "avatar" in userA:
            response = make_response(userA["avatar"])
            response.headers.set('Content-Type', 'image/svg+xml')
            return response
        else:
            # Return default avatar
            with open('default-avatar.svg', 'r') as f:
                default_avatar = f.read()
            response = make_response(default_avatar)
            response.headers.set('Content-Type', 'image/svg+xml')
            return response
    except Exception as e:
        return {"status": "failed", "message": "Failed to get avatar"}, 500

@app.route('/api/upload-avatar', methods=['POST'])
def upload_avatar():
    if 'file' not in request.files:
        return jsonify({'status': 'failed', 'message': '没有文件被上传'})
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'status': 'failed', 'message': '没有选择文件'})
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        content_type = mimetypes.guess_type(filename)[0]
        
        # 存储文件到MongoDB
        file_id = fs.put(
            file,
            filename=filename,
            content_type=content_type,
            metadata={
                'fileType': 'avatar',
                'originalName': filename,
                'uploadTime': datetime.now()
            }
        )
        
        # 更新用户头像信息
        user_id = request.form.get('user_id')
        mongodb.users.update_one(
            {'_id': ObjectId(user_id)},
            {'$set': {'avatar': file_id}}
        )
        
        return jsonify({'status': 'success', 'message': '头像上传成功'})
    
    return jsonify({'status': 'failed', 'message': '不支持的文件类型'})

if __name__ == '__main__':
    app.run(debug=True)
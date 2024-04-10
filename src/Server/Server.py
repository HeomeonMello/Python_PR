#server.py
from flask import Flask, request, jsonify
from src.DB import db_connection
from flask_jwt_extended import JWTManager, create_access_token,jwt_required, get_jwt_identity

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'your-secret-key'  # JWT를 위한 시크릿 키
jwt = JWTManager(app)
@app.route('/ping', methods=['GET'])
def ping():
    """서버 상태 확인을 위한 함수"""
    db_connected = db_connection.check_db_connection()
    if db_connected:
        return jsonify({'message': 'pong', 'db_status': 'connected'}), 200
    else:
        return jsonify({'message': 'pong', 'db_status': 'disconnected'}), 500

@app.route('/register', methods=['POST'])
def register():
    """서버 사용자 등록을 위한 함수"""
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')  # 비밀번호를 그대로 사용합니다.
    userid = data.get('userid')  # 사용자의 id
    interests = data.get('interests', [])  # 사용자의 관심사 목록

    if db_connection.register_user(username, password, userid, interests):
        return jsonify({'message': 'User registered successfully'}), 201
    else:
        return jsonify({'message': "Registration failed"}), 400

@app.route('/login', methods=['POST'])
def login():
    """로그인 요청을 처리하는 함수"""
    data = request.get_json()
    userid = data.get('username')
    password = data.get('password')  # 비밀번호를 그대로 사용합니다.

    if db_connection.login(userid, password):
        access_token = create_access_token(identity=userid)
        return jsonify({'message': 'Login successful', 'access_token': access_token}), 200
    else:
        return jsonify({'message': 'Invalid username or password'}), 401


@app.route('/userinfo', methods=['GET'])
@jwt_required()
def get_user_info():
    """사용자 정보를 조회하는 함수"""
    current_user_id = get_jwt_identity()  # JWT 토큰에서 사용자 ID 추출
    user_info = db_connection.get_user_info_by_userid(current_user_id)

    if user_info:
        # 사용자의 관심사 정보도 포함하여 반환
        return jsonify(user_info), 200
    else:
        return jsonify({'message': 'User not found'}), 404

if __name__ == '__main__':
    app.run(debug=True, port=5000)


from flask import Flask, request, jsonify

app = Flask(__name__)

# 사전 정의된 사용자 정보 (실제 애플리케이션에서는 데이터베이스 등에서 관리)
users = {
    'user1': 'password1',
    'user2': 'password2',
}

@app.route('/ping', methods=['GET'])
def ping():
    """서버 상태 확인을 위한 경로"""
    return jsonify({'message': 'pong'}), 200

@app.route('/login', methods=['POST'])
def login():
    """로그인 요청을 처리하는 경로"""
    data = request.get_json()  # 클라이언트로부터 받은 JSON 데이터
    username = data.get('username')
    password = data.get('password')

    # 사용자 인증 로직
    if username in users and users[username] == password:
        return jsonify({'message': 'Login successful'}), 200
    else:
        return jsonify({'message': 'Invalid username or password'}), 401

if __name__ == '__main__':
    app.run(debug=True, port=5000)

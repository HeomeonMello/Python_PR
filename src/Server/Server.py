#server.py
from flask import Flask, request, jsonify
from src.DB import db_connection
from src.main.Algorithm import recommend_articles
from src.main.API import (get_politics_headlines, get_Economy_headlines,
                          get_Society_headlines, get_IT_headlines, get_Car_headlines, get_Life_headlines, get_World_headlines, get_Fashion_headlines,
                          get_Exhibition_headlines, get_Travel_headlines, get_Health_headlines, get_Food_headlines, get_Book_headlines,
                          get_Religion_headlines, get_entertainment_headlines,  get_Breaking_headlines)
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

@app.route('/update_interests', methods=['PUT'])
@jwt_required()
def update_interests():
    """사용자 관심사를 업데이트하는 함수"""
    current_user_id = get_jwt_identity()  # JWT 토큰에서 사용자 ID 추출
    data = request.get_json()
    new_interests = data.get('interests', [])  # 사용자가 입력한 새로운 관심사 목록
    print(current_user_id,new_interests)
    if db_connection.update_user_interests(current_user_id, new_interests):
        return jsonify({'message': 'User interests updated successfully'}), 200
    else:
        return jsonify({'message': 'Failed to update interests'}), 400

@app.route('/save_click', methods=['POST'])
@jwt_required()
def save_click():
    data = request.get_json()
    user_id = data.get('user_id')
    news_title = data.get('news_title')
    news_description = data.get('news_description')
    news_url = data.get('news_url')
    publish_time = data.get('publish_time')
    current_user_id = get_jwt_identity()  # JWT 토큰에서 사용자 ID 추출

    if current_user_id != user_id:
        return jsonify({'message': 'Unauthorized access'}), 401

    if db_connection.save_user_click(user_id, news_title, news_description, news_url, publish_time):
        return jsonify({'message': 'Click saved successfully'}), 200
    else:
        return jsonify({'message': 'Failed to save click'}), 500


@app.route('/scrape_and_store', methods=['POST'])
def scrape_and_store():
    """스크래핑하여 모든 뉴스 기사를 데이터베이스에 저장하는 함수"""
    sections = [
        get_politics_headlines,
        get_Economy_headlines,
        get_Society_headlines,
        get_Life_headlines,
        get_Car_headlines,
        get_IT_headlines,
        get_World_headlines,
        get_Health_headlines,
        get_Travel_headlines,
        get_Food_headlines,
        get_Fashion_headlines,
        get_Exhibition_headlines,
        get_Book_headlines,
        get_Religion_headlines,
        get_entertainment_headlines,
        get_Breaking_headlines
    ]

    for section in sections:
        headlines = section()
        for headline in headlines:
            db_connection.insert_all_news_articles(
                headline['title'],
                headline['link'],
                headline['image_url'],
                headline['summary']
            )
    return jsonify({'message': 'News articles scraped and stored successfully'}), 200

@app.route('/user_data', methods=['GET'])
@jwt_required()
def get_user_data():
    """사용자 관심사, 클릭한 기사 및 모든 기사를 조회하는 함수"""
    current_user_id = get_jwt_identity()  # JWT 토큰에서 사용자 ID 추출
    user_id = db_connection.get_user_id_by_name(current_user_id)

    if not user_id:
        return jsonify({'message': 'User not found'}), 404

    interests, clicks, all_articles = db_connection.get_user_interests_and_clicks_and_all_articles(current_user_id)

    if interests is None or clicks is None or all_articles is None:
        return jsonify({'message': 'Failed to retrieve user data'}), 500

    return jsonify({
        'interests': interests,
        'clicks': [{'title': click[0], 'description': click[1], 'url': click[2], 'click_time': click[3]} for click in
                   clicks],
        'all_articles': [{'id': article[0], 'title': article[1], 'description': article[2], 'url': article[3]} for
                         article in all_articles]
    }), 200

@app.route('/recommendations', methods=['GET'])
@jwt_required()
def recommendations():
    current_user_name = get_jwt_identity()  # JWT 토큰에서 사용자 name 추출
    user_info = db_connection.get_user_info_by_userid(current_user_name)

    if not user_info:
        return jsonify({'message': 'User not found'}), 404

    recommended_articles = recommend_articles(current_user_name)

    if recommended_articles:
        return jsonify(recommended_articles), 200
    else:
        return jsonify({'message': 'No recommendations available'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)


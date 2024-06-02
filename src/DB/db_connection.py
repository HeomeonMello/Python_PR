# db_connection.py
import cx_Oracle
import bcrypt
from dateutil import parser
from src.DB.DB_config import db_config

def get_db_connection():
    try:
        dsn = cx_Oracle.makedsn(db_config['host'], db_config['port'], sid=db_config['sid'])
        connection = cx_Oracle.connect(
            user='system',
            password=db_config['password'],
            dsn=dsn,
            encoding=db_config['encoding']
        )
        print("Database connection successful")
        return connection
    except cx_Oracle.DatabaseError as e:
        print(f"Database connection failed: {e}")
        return None
get_db_connection()
def check_db_connection():
    connection = get_db_connection()
    if connection is not None:
        connection.close()
        return True
    else:
        return False
# 데이터베이스 연결 설정
dsn = cx_Oracle.makedsn(db_config['host'], db_config['port'], sid=db_config['sid'])
connection = cx_Oracle.connect(user='system', password=db_config['password'], dsn=dsn,encoding=db_config['encoding'])

# 새로운 사용자를 등록하는 함수
def register_user(username, password, userid, interests):
    connection = get_db_connection()
    if connection is None:
        print("데이터베이스 연결 실패")
        return False

    cursor = connection.cursor()

    # userid(name) 중복 검사
    cursor.execute("""
        SELECT COUNT(*) FROM User_Users WHERE name = :userid
    """, userid=userid)
    (user_count,) = cursor.fetchone()
    if user_count > 0:
        print("오류: userid '{userid}'는 이미 사용 중입니다.")
        return False

    # 비밀번호 해싱
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    # 사용자 정보 저장
    user_id_var = cursor.var(cx_Oracle.NUMBER)
    cursor.execute("""
        INSERT INTO User_Users (username, password, name)
        VALUES (:username, :hashed_password, :userid)
        RETURNING id INTO :user_id
    """, username=username, hashed_password=hashed_password, userid=userid, user_id=user_id_var)
    user_id = user_id_var.getvalue()[0]

    # 관심사 정보 저장
    for interest in interests:
        cursor.execute("SELECT id FROM User_Interests WHERE interestName = :interestName", interestName=interest)
        interest_id = None
        interest_row = cursor.fetchone()
        if interest_row:
            interest_id = interest_row[0]
        else:
            # 관심사가 존재하지 않는 경우, 새로운 관심사를 추가
            cursor.execute("""
                INSERT INTO User_Interests (interestName)
                VALUES (:interestName)
                RETURNING id INTO :interest_id
            """, interestName=interest, interest_id=cursor.var(cx_Oracle.NUMBER))
            interest_id = cursor.var(cx_Oracle.NUMBER).getvalue()[0]

        # 사용자와 관심사 매핑
        cursor.execute("""
            INSERT INTO User_UserInterests (userID, interestID)
            VALUES (:userID, :interestID)
        """, userID=user_id, interestID=interest_id)

    connection.commit()
    cursor.close()
    return True

def login(userid, password):
    connection = get_db_connection()
    if connection is None:
        return False

    cursor = connection.cursor()

    # 사용자 이름과 일치하는 사용자 검색
    cursor.execute("""
        SELECT password FROM User_Users WHERE name = :userid
    """, userid=userid)
    user = cursor.fetchone()

    if user and bcrypt.checkpw(password.encode('utf-8'), user[0].encode('utf-8')):
        print("로그인 성공")
        return True
    else:
        print("로그인 실패: 사용자명 또는 비밀번호가 잘못되었습니다.")
        return False
def get_user_info_by_userid(userid):
    """주어진 userid를 이용하여 사용자 정보 및 그의 관심사를 조회합니다."""
    connection = get_db_connection()
    if connection is None:
        print("데이터베이스 연결 실패")
        return None

    cursor = connection.cursor()

    # 주어진 userid에 해당하는 사용자 정보 및 그의 관심사 정보 조회
    cursor.execute("""
        SELECT u.id, u.username, u.name, i.interestName
        FROM User_Users u
        LEFT JOIN User_UserInterests ui ON u.id = ui.userID
        LEFT JOIN User_Interests i ON ui.interestID = i.id
        WHERE u.name = :userid
    """, userid=userid)

    user_info_rows = cursor.fetchall()

    if user_info_rows:
        # 사용자 정보 및 관심사 정보를 사전 형태로 가공하여 반환
        user_dict = {
            "id": user_info_rows[0][0],
            "username": user_info_rows[0][1],
            "UserID": user_info_rows[0][2],
            "interests": [row[3] for row in user_info_rows if row[3] is not None]  # 관심사가 None이 아닌 경우만 추가
        }
        return user_dict
    else:
        # 사용자 정보가 존재하지 않는 경우, None 반환
        print("사용자 정보를 찾을 수 없습니다.")
        return None

    cursor.close()


def update_user_interests(userid, new_interests):
    """ 사용자의 관심사를 업데이트하는 함수 """
    connection = get_db_connection()
    if connection is None:
        print("데이터베이스 연결 실패")
        return False

    cursor = connection.cursor()

    try:
        # 사용자 ID 조회
        cursor.execute("SELECT id FROM User_Users WHERE name = :name", {'name': userid})
        user_id_result = cursor.fetchone()
        if not user_id_result:
            print("사용자 ID가 존재하지 않습니다.")
            return False
        user_id = user_id_result[0]

        # 기존 관심사 매핑 삭제
        cursor.execute("DELETE FROM User_UserInterests WHERE userID = :userID", {'userID': user_id})

        # 새로운 관심사 추가
        for interest in new_interests:
            # 관심사가 이미 존재하는지 확인
            cursor.execute("SELECT id FROM User_Interests WHERE interestName = :interestName",
                           {'interestName': interest})
            interest_id_result = cursor.fetchone()

            if interest_id_result:
                interest_id = interest_id_result[0]
            else:
                # 관심사 추가
                new_interest_id = cursor.var(cx_Oracle.NUMBER)
                cursor.execute("""
                    INSERT INTO User_Interests (interestName)
                    VALUES (:interestName)
                    RETURNING id INTO :new_interest_id
                """, {'interestName': interest, 'new_interest_id': new_interest_id})
                interest_id = new_interest_id.getvalue()[0]  # 반환된 ID 값을 추출

            # 사용자와 관심사 매핑 추가
            cursor.execute("""
                INSERT INTO User_UserInterests (userID, interestID)
                VALUES (:userID, :interestID)
            """, {'userID': user_id, 'interestID': interest_id})

        connection.commit()
        print("관심사 업데이트 성공")
        return True

    except Exception as e:
        print(f"관심사 업데이트 실패: {e}")
        connection.rollback()
        return False

    finally:
        cursor.close()
        connection.close()

def save_user_click(user_id, news_title, news_description, news_url, publish_time):
    connection = get_db_connection()
    if connection is None:
        print("데이터베이스 연결 실패")
        return False

    cursor = connection.cursor()

    try:
        # user_id로 User_Users 테이블에서 실제 사용자 ID를 조회
        cursor.execute("SELECT id FROM User_Users WHERE name = :user_id", {'user_id': user_id})
        result = cursor.fetchone()
        if result is None:
            print("사용자를 찾을 수 없습니다.")
            return False
        actual_user_id = result[0]

        # publish_time을 올바른 형식으로 변환
        if publish_time:
            publish_time = parser.parse(publish_time).strftime('%Y-%m-%d %H:%M:%S')
        else:
            publish_time = None

        print(f"Parsed publish_time: {publish_time}")  # 디버깅을 위한 출력

        # 뉴스 ID를 저장할 변수 생성
        news_id_var = cursor.var(cx_Oracle.NUMBER)

        # 기사를 저장하고 ID를 반환받기
        cursor.execute("""
            INSERT INTO User_NewsArticles (title, description, url, publishTime)
            VALUES (:title, :description, :url, TO_TIMESTAMP(:publishTime, 'YYYY-MM-DD HH24:MI:SS'))
            RETURNING id INTO :news_id
        """, {
            'title': news_title,
            'description': news_description,
            'url': news_url,
            'publishTime': publish_time,
            'news_id': news_id_var
        })
        news_id = news_id_var.getvalue()[0]

        print(f"Returned news_id: {news_id}")  # 디버깅을 위한 출력

        # 사용자 클릭 정보 저장
        cursor.execute("""
            INSERT INTO User_UserNewsClicks (userID, newsID)
            VALUES (:userID, :newsID)
        """, {'userID': actual_user_id, 'newsID': news_id})

        connection.commit()
        print("뉴스 클릭 정보 저장 성공")
        return True

    except cx_Oracle.DatabaseError as e:
        print(f"뉴스 클릭 정보 저장 실패: {e}")
        connection.rollback()
        return False

    finally:
        cursor.close()
        connection.close()
def get_user_id_by_name(user_id):
    connection = get_db_connection()
    if connection is None:
        print("Database connection failed")
        return None

    cursor = connection.cursor()

    try:
        cursor.execute("SELECT id FROM User_Users WHERE name = :username", {'username': user_id})
        result = cursor.fetchone()
        if result:
            return result[0]
        else:
            print(f"User with name {user_id} not found")
            return None

    except cx_Oracle.DatabaseError as e:
        print(f"Database query failed: {e}")
        return None

    finally:
        cursor.close()
        connection.close()

def insert_all_news_articles(title, link, image_url, summary):
    connection = get_db_connection()
    if connection is None:
        print("Database connection failed")
        return False

    cursor = connection.cursor()

    try:
        # 중복된 타이틀이 있는지 확인
        cursor.execute("SELECT COUNT(*) FROM All_NewsArticles WHERE title = :title", {'title': title})
        count = cursor.fetchone()[0]
        if count > 0:
            print(f"Duplicate title found: {title}, skipping insertion")
            return False

        cursor.execute("""
            INSERT INTO All_NewsArticles (title, link, image_url, summary)
            VALUES (:title, :link, :image_url, :summary)
        """, {
            'title': title,
            'link': link,
            'image_url': image_url,
            'summary': summary
        })

        connection.commit()
        print("News article inserted successfully")
        return True

    except cx_Oracle.DatabaseError as e:
        print(f"Failed to insert news article: {e}")
        connection.rollback()
        return False

    finally:
        cursor.close()
        connection.close()

def get_user_interests_and_clicks_and_all_articles(user_id):
    user_id = get_user_id_by_name(user_id)
    if user_id is None:
        return None, None, None

    connection = get_db_connection()
    if connection is None:
        print("Database connection failed")
        return None, None, None

    cursor = connection.cursor()

    try:
        # 사용자 관심사 조회
        cursor.execute("""
            SELECT ui.interestName
            FROM User_UserInterests uui
            JOIN User_Interests ui ON uui.interestID = ui.id
            WHERE uui.userID = :user_id
        """, {'user_id': user_id})
        interests = [row[0] for row in cursor.fetchall()]

        # 사용자 클릭한 뉴스 기사 조회
        cursor.execute("""
            SELECT una.title, una.description, una.url, uunc.clickTime
            FROM User_UserNewsClicks uunc
            JOIN User_NewsArticles una ON uunc.newsID = una.id
            WHERE uunc.userID = :user_id
        """, {'user_id': user_id})
        clicks = cursor.fetchall()

        # 모든 뉴스 기사 조회
        cursor.execute("SELECT id, title, description, url FROM All_NewsArticles")
        all_articles = cursor.fetchall()

        return interests, clicks, all_articles

    except cx_Oracle.DatabaseError as e:
        print(f"Database query failed: {e}")
        return None, None, None

    finally:
        cursor.close()
        connection.close()

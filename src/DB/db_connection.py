# db_connection.py
import cx_Oracle
from DB_config import db_config
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
# 데이터베이스 연결 설정
dsn = cx_Oracle.makedsn('localhost', 1521, sid=db_config['sid'])
connection = cx_Oracle.connect(user='system', password=db_config['password'], dsn=dsn)

def register_user(username, password, name, interests):
    """새로운 사용자를 등록하는 함수"""
    cursor = connection.cursor()

    # User_Users 테이블에 사용자 정보 추가
    cursor.execute("""
        INSERT INTO User_Users (username, password, name)
        VALUES (:username, :password, :name)
    """, username=username, password=password, name=name)

    user_id = cursor.lastrowid  # 새로 생성된 사용자 ID 가져오기

    # 관심사 정보를 User_Interests와 User_UserInterests에 추가
    for interest in interests:
        cursor.execute("""
            SELECT id FROM User_Interests WHERE interestName = :interestName
        """, interestName=interest)
        interest_row = cursor.fetchone()

        if interest_row is None:
            # 관심사가 존재하지 않으면 새로 추가
            cursor.execute("""
                INSERT INTO User_Interests (interestName)
                VALUES (:interestName)
            """, interestName=interest)
            interest_id = cursor.lastrowid
        else:
            interest_id = interest_row[0]

        # 사용자와 관심사 연결
        cursor.execute("""
            INSERT INTO User_UserInterests (userID, interestID)
            VALUES (:userID, :interestID)
        """, userID=user_id, interestID=interest_id)

    connection.commit()
    cursor.close()


def register_user(username, password, name, interests):
    """새로운 사용자를 등록하는 함수"""
    cursor = connection.cursor()

    # User_Users 테이블에 사용자 정보 추가
    cursor.execute("""
        INSERT INTO User_Users (username, password, name)
        VALUES (:username, :password, :name)
    """, username=username, password=password, name=name)

    user_id = cursor.lastrowid  # 새로 생성된 사용자 ID 가져오기

    # 관심사 정보를 User_Interests와 User_UserInterests에 추가
    for interest in interests:
        cursor.execute("""
            SELECT id FROM User_Interests WHERE interestName = :interestName
        """, interestName=interest)
        interest_row = cursor.fetchone()

        if interest_row is None:
            # 관심사가 존재하지 않으면 새로 추가
            cursor.execute("""
                INSERT INTO User_Interests (interestName)
                VALUES (:interestName)
            """, interestName=interest)
            interest_id = cursor.lastrowid
        else:
            interest_id = interest_row[0]

        # 사용자와 관심사 연결
        cursor.execute("""
            INSERT INTO User_UserInterests (userID, interestID)
            VALUES (:userID, :interestID)
        """, userID=user_id, interestID=interest_id)

    connection.commit()
    cursor.close()


def login(username, password):
    """사용자 로그인을 처리하는 함수"""
    cursor = connection.cursor()
    cursor.execute("""
        SELECT id FROM User_Users WHERE username = :username AND password = :password
    """, username=username, password=password)

    user_row = cursor.fetchone()
    cursor.close()

    if user_row:
        print("로그인 성공")
        return True
    else:
        print("로그인 실패: 사용자명 또는 비밀번호가 잘못되었습니다.")
        return False


def save_user_click(user_id, news_id):
    """사용자가 뉴스를 클릭한 정보를 저장하는 함수"""
    cursor = connection.cursor()

    # 뉴스 클릭 정보 저장
    cursor.execute("""
        INSERT INTO User_UserNewsClicks (userID, newsID)
        VALUES (:userID, :newsID)
    """, userID=user_id, newsID=news_id)

    connection.commit()
    cursor.close()
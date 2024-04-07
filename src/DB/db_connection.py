# db_connection.py
import cx_Oracle
import bcrypt
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
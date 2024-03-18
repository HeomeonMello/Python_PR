import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="로컬 파일 기반 DB 및 서버-클라이언트 아키텍처를 사용하는 애플리케이션.")
    parser.add_argument('--db', type=str, default='app.db', help='데이터베이스 파일 경로')
    parser.add_argument('--mode', type=str, choices=['server', 'client'], required=True, help='실행 모드 선택 (server/client)')
    parser.add_argument('--port', type=int, default=8080, help='서버 모드에서 사용할 포트')
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()
    print(f"모드: {args.mode}, DB 파일: {args.db}, 포트: {args.port}")
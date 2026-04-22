# pip install pymysql cryptography

import os
import pymysql
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

def getConnection():
    """ MySQL 데이터베이스 연결을 생성하여 반환합니다. """
    return pymysql.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

def saveAnalysisResult(fileName, question, answer, modelName):
    """ 분석 결과를 MySQL 데이터베이스에 저장합니다. """
    connection = None
    try:
        connection = getConnection()
        with connection.cursor() as cursor:
            # 테이블이 없는 경우 생성 (분석결과 저장용)
            createTableSql = \"\"\"
            CREATE TABLE IF NOT EXISTS analysis_results (
                id INT AUTO_INCREMENT PRIMARY KEY,
                file_name VARCHAR(255),
                question TEXT,
                answer TEXT,
                model_name VARCHAR(50),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            \"\"\"
            cursor.execute(createTableSql)
            
            # 데이터 삽입
            insertSql = \"\"\"
            INSERT INTO analysis_results (file_name, question, answer, model_name)
            VALUES (%s, %s, %s, %s)
            \"\"\"
            cursor.execute(insertSql, (fileName, question, answer, modelName))
            
        connection.commit()
        return True
        
    except Exception as e:
        if connection:
            connection.rollback()
        print(f"DB 저장 에러: {str(e)}")
        return False
        
    finally:
        if connection:
            connection.close()

def getAllResults():
    """ 저장된 모든 분석 결과를 조회합니다. """
    connection = None
    results = []
    try:
        connection = getConnection()
        with connection.cursor() as cursor:
            sql = "SELECT * FROM analysis_results ORDER BY created_at DESC"
            cursor.execute(sql)
            rows = cursor.fetchall()
            
            # 리스트 컴프리헨션 대신 명시적 for 루프 사용 (가이드 준수)
            for i in range(0, len(rows)):
                results.append(rows[i])
                
        return results
        
    except Exception as e:
        print(f"DB 조회 에러: {str(e)}")
        return []
        
    finally:
        if connection:
            connection.close()

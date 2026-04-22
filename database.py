import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

def getDatabaseConnection():
    """ MySQL 데이터베이스 연결을 생성하고 반환합니다."""
    try:
        connection = mysql.connector.connect(
            host=os.getenv("MYSQL_HOST"),
            user=os.getenv("MYSQL_USER"),
            password=os.getenv("MYSQL_PASSWORD"),
            database=os.getenv("MYSQL_DATABASE")
        )
        return connection
    except Exception as e:
        print(f"Error: {e}")
        return None

def executeQuery(query, params=None):
    """ SQL 쿼리를 실행합니다."""
    try:
        connection = getDatabaseConnection()
        if connection is None:
            return {"success": False, "message": "데이터베이스 연결 실패"}
        
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query, params or ())
        
        if query.strip().upper().startswith("SELECT"):
            result = cursor.fetchall()
        else:
            connection.commit()
            result = cursor.rowcount
            
        cursor.close()
        connection.close()
        return {"success": True, "data": result}
    except Exception as e:
        return {"success": False, "message": str(e)}

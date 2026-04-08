"""
Utility script to create or reset admin account
Usage: python reset_admin.py
"""
from werkzeug.security import generate_password_hash
import mysql.connector
from config import Config

def get_db_connection():
    return mysql.connector.connect(
        host=Config.MYSQL_HOST,
        port=Config.MYSQL_PORT,
        user=Config.MYSQL_USER,
        password=Config.MYSQL_PASSWORD,
        database=Config.MYSQL_DATABASE
    )

def reset_admin():
    ma_qt = "QT001"
    ho_ten = "Administrator"
    email = "admin@qlsvsdh.com"
    password = "admin123"

    password_hash = generate_password_hash(password)

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT ma_qt FROM quan_tri WHERE ma_qt = %s", (ma_qt,))
        existing = cursor.fetchone()

        if existing:
            cursor.execute("""
                UPDATE quan_tri
                SET password_hash = %s, ho_ten = %s, email = %s
                WHERE ma_qt = %s
            """, (password_hash, ho_ten, email, ma_qt))
            print("SUCCESS: Updated existing admin account")
        else:
            cursor.execute("""
                INSERT INTO quan_tri (ma_qt, ho_ten, email, password_hash)
                VALUES (%s, %s, %s, %s)
            """, (ma_qt, ho_ten, email, password_hash))
            print("SUCCESS: Created new admin account")

        conn.commit()

        print("\n" + "="*50)
        print("Admin credentials:")
        print("="*50)
        print(f"Email:    {email}")
        print(f"Password: {password}")
        print(f"ma_qt:    {ma_qt}")
        print("="*50)
        print("\nYou can now login with these credentials.")

    except Exception as e:
        conn.rollback()
        print(f"ERROR: {e}")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    reset_admin()

"""
BaseModel - Base class cho tất cả Models
Cung cấp kết nối MySQL và CRUD helpers sử dụng mysql-connector-python
"""
import mysql.connector
from mysql.connector import Error
from typing import Optional, List, Dict, Any

from config import Config


class BaseModel:
    """Base Model với CRUD operations"""

    table_name: str = ""
    primary_key: str = "id"

    def __init__(self):
        self.cnx = None
        self.cursor = None

    # ========== Database Connection ==========

    @classmethod
    def get_connection(cls):
        """Tạo kết nối MySQL mới"""
        try:
            cnx = mysql.connector.connect(
                host=Config.MYSQL_HOST,
                port=Config.MYSQL_PORT,
                user=Config.MYSQL_USER,
                password=Config.MYSQL_PASSWORD,
                database=Config.MYSQL_DATABASE,
                charset="utf8mb4",
                collation="utf8mb4_unicode_ci"
            )
            return cnx
        except Error as e:
            raise ConnectionError(f"Lỗi kết nối MySQL: {e}")

    @classmethod
    def get_cursor(cls, dictionary=True):
        """Lấy cursor từ connection"""
        cnx = cls.get_connection()
        cursor = cnx.cursor(dictionary=dictionary)
        return cnx, cursor

    # ========== CRUD Operations ==========

    @classmethod
    def find(cls, pk_value: Any) -> Optional[Dict[str, Any]]:
        """Tìm bản ghi theo primary key"""
        cnx, cursor = cls.get_cursor()
        try:
            query = f"SELECT * FROM {cls.table_name} WHERE {cls.primary_key} = %s"
            cursor.execute(query, (pk_value,))
            result = cursor.fetchone()
            return result
        finally:
            cursor.close()
            cnx.close()

    @classmethod
    def all(cls, order_by: str = None, limit: int = None) -> List[Dict[str, Any]]:
        """Lấy tất cả bản ghi"""
        cnx, cursor = cls.get_cursor()
        try:
            query = f"SELECT * FROM {cls.table_name}"
            if order_by:
                query += f" ORDER BY {order_by}"
            if limit:
                query += f" LIMIT {limit}"
            cursor.execute(query)
            results = cursor.fetchall()
            return results
        finally:
            cursor.close()
            cnx.close()

    @classmethod
    def where(cls, conditions: Dict[str, Any], order_by: str = None) -> List[Dict[str, Any]]:
        """Tìm theo điều kiện"""
        cnx, cursor = cls.get_cursor()
        try:
            where_clause = " AND ".join([f"{k} = %s" for k in conditions.keys()])
            query = f"SELECT * FROM {cls.table_name} WHERE {where_clause}"
            if order_by:
                query += f" ORDER BY {order_by}"
            cursor.execute(query, tuple(conditions.values()))
            return cursor.fetchall()
        finally:
            cursor.close()
            cnx.close()

    @classmethod
    def create(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        """Tạo bản ghi mới"""
        cnx, cursor = cls.get_cursor()
        try:
            columns = ", ".join(data.keys())
            placeholders = ", ".join(["%s"] * len(data))
            query = f"INSERT INTO {cls.table_name} ({columns}) VALUES ({placeholders})"
            cursor.execute(query, tuple(data.values()))
            cnx.commit()
            # Lấy bản ghi vừa tạo
            if cls.primary_key != "id":
                pk_value = data.get(cls.primary_key)
            else:
                pk_value = cursor.lastinsertid
            return cls.find(pk_value)
        finally:
            cursor.close()
            cnx.close()

    @classmethod
    def update(cls, pk_value: Any, data: Dict[str, Any]) -> Dict[str, Any]:
        """Cập nhật bản ghi"""
        cnx, cursor = cls.get_cursor()
        try:
            set_clause = ", ".join([f"{k} = %s" for k in data.keys()])
            query = f"UPDATE {cls.table_name} SET {set_clause} WHERE {cls.primary_key} = %s"
            cursor.execute(query, tuple(data.values()) + (pk_value,))
            cnx.commit()
            return cls.find(pk_value)
        finally:
            cursor.close()
            cnx.close()

    @classmethod
    def delete(cls, pk_value: Any) -> bool:
        """Xóa bản ghi"""
        cnx, cursor = cls.get_cursor()
        try:
            query = f"DELETE FROM {cls.table_name} WHERE {cls.primary_key} = %s"
            cursor.execute(query, (pk_value,))
            cnx.commit()
            return cursor.rowcount > 0
        finally:
            cursor.close()
            cnx.close()

    @classmethod
    def exists(cls, pk_value: Any) -> bool:
        """Kiểm tra bản ghi tồn tại"""
        cnx, cursor = cls.get_cursor()
        try:
            query = f"SELECT 1 FROM {cls.table_name} WHERE {cls.primary_key} = %s"
            cursor.execute(query, (pk_value,))
            return cursor.fetchone() is not None
        finally:
            cursor.close()
            cnx.close()

    @classmethod
    def count(cls, conditions: Dict[str, Any] = None) -> int:
        """Đếm số bản ghi"""
        cnx, cursor = cls.get_cursor()
        try:
            if conditions:
                where_clause = " AND ".join([f"{k} = %s" for k in conditions.keys()])
                query = f"SELECT COUNT(*) as cnt FROM {cls.table_name} WHERE {where_clause}"
                cursor.execute(query, tuple(conditions.values()))
            else:
                query = f"SELECT COUNT(*) as cnt FROM {cls.table_name}"
                cursor.execute(query)
            return cursor.fetchone()["cnt"]
        finally:
            cursor.close()
            cnx.close()

    # ========== Transaction Helpers ==========

    @classmethod
    def transaction(cls, callback):
        """Thực hiện transaction"""
        cnx, cursor = cls.get_cursor()
        try:
            result = callback(cnx, cursor)
            cnx.commit()
            return result
        except Exception as e:
            cnx.rollback()
            raise e
        finally:
            cursor.close()
            cnx.close()

    @classmethod
    def raw_query(cls, query: str, params: tuple = None, fetch_one: bool = False):
        """Chạy raw SQL query"""
        cnx, cursor = cls.get_cursor()
        try:
            cursor.execute(query, params or ())
            if fetch_one:
                return cursor.fetchone()
            return cursor.fetchall()
        finally:
            cursor.close()
            cnx.close()

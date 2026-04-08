"""
QuanTri Model - Bảng quan_tri (Admin)
"""
from app.models.base import BaseModel


class QuanTri(BaseModel):
    table_name = "quan_tri"
    primary_key = "ma_qt"  # Actual DB column: ma_qt VARCHAR(20) PK

    @classmethod
    def find_by_username(cls, email: str):
        """Tìm admin theo email (login username)"""
        return cls.raw_query(
            "SELECT * FROM quan_tri WHERE email = %s",
            (email,),
            fetch_one=True
        )

    @classmethod
    def get_all_admins(cls, order_by: str = None):
        """Lấy tất cả admin"""
        return cls.all(order_by=order_by or "ma_qt")

    @classmethod
    def get_by_id(cls, ma_qt: str):
        """Lấy admin theo ma_qt"""
        return cls.find(ma_qt)

    @classmethod
    def create_admin(cls, data: dict):
        """Tạo admin mới"""
        return cls.create(data)

    @classmethod
    def update_admin(cls, ma_qt: str, data: dict):
        """Cập nhật admin"""
        return cls.update(ma_qt, data)

    @classmethod
    def delete_admin(cls, ma_qt: str):
        """Xóa admin"""
        return cls.delete(ma_qt)
"""
QuanTri Model - Bảng quan_tri (Admin)
"""
from app.models.base import BaseModel


class QuanTri(BaseModel):
    table_name = "quan_tri"
    primary_key = "ma_qt"

    @classmethod
    def find_by_username(cls, ten_dn: str):
        """Tìm admin theo tên đăng nhập (email)"""
        return cls.raw_query(
            "SELECT * FROM quan_tri WHERE email = %s",
            (ten_dn,),
            fetch_one=True
        )

    @classmethod
    def get_thong_bao_by_admin(cls, ma_admin: str):
        """Lấy thông báo do admin tạo"""
        return cls.raw_query(
            "SELECT * FROM thong_bao WHERE ma_admin = %s",
            (ma_admin,)
        )

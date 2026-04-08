"""
Lop Model - Bảng lop (Class)
"""
from app.models.base import BaseModel


class Lop(BaseModel):
    table_name = "lop"
    primary_key = "ma_lop"

    @classmethod
    def get_nganh(cls, ma_lop: str):
        """Lấy thông tin ngành của lớp"""
        result = cls.raw_query(
            """SELECT n.* FROM nganh n
               INNER JOIN lop l ON n.ma_nganh = l.ma_nganh
               WHERE l.ma_lop = %s""",
            (ma_lop,),
            fetch_one=True
        )
        return result

    @classmethod
    def get_sinh_vien(cls, ma_lop: str):
        """Lấy danh sách sinh viên thuộc lớp"""
        return cls.raw_query(
            "SELECT * FROM sinh_vien WHERE ma_lop = %s",
            (ma_lop,)
        )

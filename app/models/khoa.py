"""
Khoa Model - Bảng khoa (Faculty/Department)
"""
from app.models.base import BaseModel


class Khoa(BaseModel):
    table_name = "khoa"
    primary_key = "ma_khoa"  # Actual DB column

    @classmethod
    def get_nganh(cls, ma_khoa: str):
        """Lấy danh sách ngành thuộc khoa"""
        return cls.raw_query(
            "SELECT * FROM nganh WHERE ma_khoa = %s",
            (ma_khoa,)
        )

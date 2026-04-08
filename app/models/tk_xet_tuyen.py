"""
TKXetTuyen Model - Bảng tk_xet_tuyen (Candidate Account)
"""
from app.models.base import BaseModel


class TKXetTuyen(BaseModel):
    table_name = "tk_xet_tuyen"
    primary_key = "ma_tk"

    @classmethod
    def find_by_email(cls, email: str):
        """Tìm tài khoản theo email"""
        return cls.raw_query(
            "SELECT * FROM tk_xet_tuyen WHERE email = %s",
            (email,),
            fetch_one=True
        )

    @classmethod
    def get_ho_so(cls, ma_tk: str):
        """Lấy hồ sơ thí sinh"""
        return cls.raw_query(
            "SELECT * FROM hso_xet_tuyen WHERE ma_tk = %s",
            (ma_tk,),
            fetch_one=True
        )

"""
Nganh Model - Bảng nganh (Major)
"""
from app.models.base import BaseModel


class Nganh(BaseModel):
    table_name = "nganh"
    primary_key = "ma_nganh"

    @classmethod
    def get_khoa(cls, ma_nganh: str):
        """Lấy thông tin khoa của ngành"""
        result = cls.raw_query(
            """SELECT k.* FROM khoa k
               INNER JOIN nganh n ON k.ma_khoa = n.ma_khoa
               WHERE n.ma_nganh = %s""",
            (ma_nganh,),
            fetch_one=True
        )
        return result

    @classmethod
    def get_lop(cls, ma_nganh: str):
        """Lấy danh sách lớp thuộc ngành"""
        return cls.raw_query(
            "SELECT * FROM lop WHERE ma_nganh = %s",
            (ma_nganh,)
        )

    @classmethod
    def get_phieu_dang_ky(cls, ma_nganh: str):
        """Lấy phiếu đăng ký xét tuyển của ngành"""
        return cls.raw_query(
            "SELECT * FROM pt_xet_tuyen WHERE ma_nganh = %s",
            (ma_nganh,)
        )

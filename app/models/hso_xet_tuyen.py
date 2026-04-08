"""
HSOXetTuyen Model - Bảng hso_xet_tuyen (Candidate Profile)
"""
from app.models.base import BaseModel


class HSOXetTuyen(BaseModel):
    table_name = "hso_xet_tuyen"
    primary_key = "ma_hs"

    @classmethod
    def get_tai_khoan(cls, ma_hs: str):
        """Lấy thông tin tài khoản thí sinh"""
        result = cls.raw_query(
            """SELECT t.* FROM tk_xet_tuyen t
               INNER JOIN hso_xet_tuyen h ON t.ma_tk = h.ma_tk
               WHERE h.ma_hs = %s""",
            (ma_hs,),
            fetch_one=True
        )
        return result

    @classmethod
    def get_phieu_dang_ky(cls, ma_hs: str):
        """Lấy danh sách phiếu đăng ký xét tuyển"""
        return cls.raw_query(
            "SELECT * FROM pt_xet_tuyen WHERE ma_tk = %s",
            (ma_hs,)
        )

    @classmethod
    def get_sinh_vien(cls, ma_hs: str):
        """Lấy sinh viên được tạo từ hồ sơ"""
        result = cls.raw_query(
            "SELECT * FROM sinh_vien WHERE ma_hs = %s",
            (ma_hs,),
            fetch_one=True
        )
        return result

"""
HSOXetTuyen Model - Bang hso_xet_tuyen (Ho so xet tuyen)
Luu tru truc tiep thong tin thi sinh (ho_ten, cccd, so_dien_thoai)
"""
from app.models.base import BaseModel


class HSOXetTuyen(BaseModel):
    table_name = "hso_xet_tuyen"
    primary_key = "ma_hs"

    @classmethod
    def get_phieu_dang_ky(cls, ma_hs: str):
        """Lay danh sach phieu dang ky xet tuyen"""
        return cls.raw_query(
            "SELECT * FROM pt_xet_tuyen WHERE ma_hs = %s",
            (ma_hs,)
        )

    @classmethod
    def get_sinh_vien(cls, ma_hs: str):
        """Lay sinh vien duoc tao tu ho so"""
        result = cls.raw_query(
            "SELECT * FROM sinh_vien WHERE ma_hs = %s",
            (ma_hs,),
            fetch_one=True
        )
        return result

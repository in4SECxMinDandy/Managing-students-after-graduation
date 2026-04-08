"""
PTXetTuyen Model - Bang pt_xet_tuyen (Phieu xet tuyen)
"""
from app.models.base import BaseModel


class PTXetTuyen(BaseModel):
    table_name = "pt_xet_tuyen"
    primary_key = "ma_pt"

    @classmethod
    def get_by_trang_thai(cls, trang_thai: str):
        """Lay phieu theo trang thai"""
        return cls.raw_query(
            "SELECT * FROM pt_xet_tuyen WHERE trang_thai = %s ORDER BY ma_pt DESC",
            (trang_thai,)
        )

    @classmethod
    def get_cho_duyet(cls):
        """Lay danh sach cho duyet"""
        return cls.get_by_trang_thai("Cho duyet")

    @classmethod
    def update_trang_thai(cls, ma_pt: str, trang_thai: str, ma_admin: str):
        """Cap nhat trang thai phieu"""
        return cls.update(ma_pt, {
            "trang_thai": trang_thai,
            "ghi_chu": f"Duyet boi: {ma_admin}"
        })

    @classmethod
    def get_all_with_details(cls):
        """Lay tat ca phieu voi thong tin chi tiet"""
        return cls.raw_query("""
            SELECT pt.*,
                   h.ho_ten as ho_ten_thi_sinh,
                   h.cccd,
                   h.so_dien_thoai,
                   n.ten_nganh,
                   k.ten_khoa
            FROM pt_xet_tuyen pt
            INNER JOIN hso_xet_tuyen h ON pt.ma_hs = h.ma_hs
            INNER JOIN nganh n ON pt.ma_nganh = n.ma_nganh
            INNER JOIN khoa k ON n.ma_khoa = k.ma_khoa
            ORDER BY pt.ma_pt DESC
        """)

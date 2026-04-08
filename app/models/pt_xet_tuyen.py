"""
PTXetTuyen Model - Bảng pt_xet_tuyen (Admission Form)
"""
from app.models.base import BaseModel


class PTXetTuyen(BaseModel):
    table_name = "pt_xet_tuyen"
    primary_key = "ma_pt"

    @classmethod
    def get_by_trang_thai(cls, trang_thai: str):
        """Lấy phiếu theo trạng thái"""
        return cls.raw_query(
            "SELECT * FROM pt_xet_tuyen WHERE trang_thai = %s ORDER BY ma_pt DESC",
            (trang_thai,)
        )

    @classmethod
    def get_cho_duyet(cls):
        """Lấy danh sách chờ duyệt"""
        return cls.get_by_trang_thai("Cho duyet")

    @classmethod
    def update_trang_thai(cls, ma_pt: str, trang_thai: str, ma_admin: str):
        """Cập nhật trạng thái phiếu"""
        return cls.update(ma_pt, {
            "trang_thai": trang_thai,
            "ghi_chu": f"Duyệt bởi: {ma_admin}"
        })

    @classmethod
    def get_all_with_details(cls):
        """Lấy tất cả phiếu với thông tin chi tiết"""
        return cls.raw_query("""
            SELECT pt.*,
                   tk.ho_ten as ho_ten_thi_sinh,
                   tk.cccd,
                   tk.so_dien_thoai,
                   n.ten_nganh,
                   k.ten_khoa
            FROM pt_xet_tuyen pt
            INNER JOIN tk_xet_tuyen tk ON pt.ma_tk = tk.ma_tk
            INNER JOIN nganh n ON pt.ma_nganh = n.ma_nganh
            INNER JOIN khoa k ON n.ma_khoa = k.ma_khoa
            ORDER BY pt.ma_pt DESC
        """)

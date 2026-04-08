"""
SinhVien Model - Bảng sinh_vien (Student)
"""
from app.models.base import BaseModel


class SinhVien(BaseModel):
    table_name = "sinh_vien"
    primary_key = "ma_sv"

    @classmethod
    def find_by_email(cls, email: str):
        """Tìm sinh viên theo email"""
        return cls.raw_query(
            "SELECT * FROM sinh_vien WHERE email = %s",
            (email,),
            fetch_one=True
        )

    @classmethod
    def get_lop(cls, ma_sv: str):
        """Lấy thông tin lớp của sinh viên"""
        result = cls.raw_query(
            """SELECT l.* FROM lop l
               INNER JOIN sinh_vien s ON l.ma_lop = s.ma_lop
               WHERE s.ma_sv = %s""",
            (ma_sv,),
            fetch_one=True
        )
        return result

    @classmethod
    def get_ket_qua_hoc_tap(cls, ma_sv: str):
        """Lấy kết quả học tập của sinh viên"""
        return cls.raw_query(
            "SELECT * FROM kq_hoc_tap WHERE ma_sv = %s",
            (ma_sv,)
        )

    @classmethod
    def get_tot_nghiep(cls, ma_sv: str):
        """Lấy thông tin tốt nghiệp"""
        result = cls.raw_query(
            "SELECT * FROM tot_nghiep WHERE ma_sv = %s",
            (ma_sv,),
            fetch_one=True
        )
        return result

    @classmethod
    def get_thong_bao(cls, ma_sv: str):
        """Lấy thông báo của sinh viên"""
        return cls.raw_query("""
            SELECT tb.*, tbn.da_doc, tbn.created_at as thoi_gian_doc
            FROM tb_nguoi_nhan tbn
            INNER JOIN thong_bao tb ON tbn.ma_tb = tb.ma_tb
            WHERE tbn.ma_nguoi_nhan = %s AND tbn.loai_nguoi_nhan = 'sinh_vien'
            ORDER BY tb.created_at DESC
        """, (ma_sv,))

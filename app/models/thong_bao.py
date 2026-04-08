"""
ThongBao Model - Bảng thong_bao (Notification)
"""
from app.models.base import BaseModel


class ThongBao(BaseModel):
    table_name = "thong_bao"
    primary_key = "ma_tb"

    @classmethod
    def get_admin(cls, ma_tb: str):
        """Lấy thông tin admin tạo thông báo"""
        result = cls.raw_query(
            """SELECT q.* FROM quan_tri q
               INNER JOIN thong_bao t ON q.ma_qt = t.nguoi_tao
               WHERE t.ma_tb = %s""",
            (ma_tb,),
            fetch_one=True
        )
        return result

    @classmethod
    def get_nguoi_nhan(cls, ma_tb: str):
        """Lay danh sach nguoi nhan thong bao"""
        return cls.raw_query("""
            SELECT tbn.*, sv.ho_ten
            FROM tb_nguoi_nhan tbn
            INNER JOIN sinh_vien sv ON tbn.ma_nguoi_nhan = sv.ma_sv
            WHERE tbn.ma_tb = %s
        """, (ma_tb,))

    @classmethod
    def get_all_with_creator(cls):
        """Lấy tất cả thông báo với tên admin tạo"""
        return cls.raw_query("""
            SELECT t.*, q.ho_ten as ten_admin
            FROM thong_bao t
            LEFT JOIN quan_tri q ON t.nguoi_tao = q.ma_qt
            ORDER BY t.created_at DESC
        """)

    @classmethod
    def mark_as_read(cls, ma_tb: str, ma_sv: str):
        """Đánh dấu đã đọc"""
        cnx, cursor = cls.get_cursor()
        try:
            cursor.execute("""
                UPDATE tb_nguoi_nhan
                SET da_doc = 1
                WHERE ma_tb = %s AND ma_nguoi_nhan = %s
            """, (ma_tb, ma_sv))
            cnx.commit()
            return True
        finally:
            cursor.close()
            cnx.close()

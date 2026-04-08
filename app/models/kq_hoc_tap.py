"""
KQHocTap Model - Bảng kq_hoc_tap (Academic Result)
Composite PK: (ma_sv, ma_mh)
"""
from app.models.base import BaseModel


class KQHocTap(BaseModel):
    table_name = "kq_hoc_tap"
    primary_key = "ma_sv"  # Composite key, primaryKey là ma_sv cho find operation

    @classmethod
    def find_by_sv_mh(cls, ma_sv: str, ma_mh: str):
        """Tìm kết quả học tập theo SV và MH"""
        return cls.raw_query(
            "SELECT * FROM kq_hoc_tap WHERE ma_sv = %s AND ma_mh = %s",
            (ma_sv, ma_mh),
            fetch_one=True
        )

    @classmethod
    def upsert(cls, ma_sv: str, ma_mh: str, diem: float):
        """Insert hoặc update điểm"""
        cnx, cursor = cls.get_cursor()
        try:
            # Kiểm tra tồn tại
            cursor.execute(
                "SELECT * FROM kq_hoc_tap WHERE ma_sv = %s AND ma_mh = %s",
                (ma_sv, ma_mh)
            )
            existing = cursor.fetchone()
            if existing:
                cursor.execute(
                    "UPDATE kq_hoc_tap SET diem = %s WHERE ma_sv = %s AND ma_mh = %s",
                    (diem, ma_sv, ma_mh)
                )
            else:
                cursor.execute(
                    "INSERT INTO kq_hoc_tap (ma_sv, ma_mh, diem) VALUES (%s, %s, %s)",
                    (ma_sv, ma_mh, diem)
                )
            cnx.commit()
            return cls.find_by_sv_mh(ma_sv, ma_mh)
        finally:
            cursor.close()
            cnx.close()

    @classmethod
    def delete_by_sv_mh(cls, ma_sv: str, ma_mh: str):
        """Xóa kết quả học tập"""
        cnx, cursor = cls.get_cursor()
        try:
            cursor.execute(
                "DELETE FROM kq_hoc_tap WHERE ma_sv = %s AND ma_mh = %s",
                (ma_sv, ma_mh)
            )
            cnx.commit()
            return cursor.rowcount > 0
        finally:
            cursor.close()
            cnx.close()

    @classmethod
    def get_all_with_mon_hoc(cls, ma_sv: str):
        """Lấy tất cả điểm với thông tin môn học"""
        return cls.raw_query("""
            SELECT kq.*, mh.ten_mh, mh.so_tin_chi
            FROM kq_hoc_tap kq
            INNER JOIN mon_hoc mh ON kq.ma_mh = mh.ma_mh
            WHERE kq.ma_sv = %s
            ORDER BY mh.ten_mh
        """, (ma_sv,))

"""
MonHoc Model - Bảng mon_hoc (Subject/Course)
"""
from app.models.base import BaseModel


class MonHoc(BaseModel):
    table_name = "mon_hoc"
    primary_key = "ma_mh"

    @classmethod
    def get_ket_qua_hoc_tap(cls, ma_mh: str):
        """Lấy danh sách kết quả học tập của môn học"""
        return cls.raw_query(
            "SELECT * FROM kq_hoc_tap WHERE ma_mh = %s",
            (ma_mh,)
        )

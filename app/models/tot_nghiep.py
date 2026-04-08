"""
TotNghiep Model - Bảng tot_nghiep (Graduation)
"""
from app.models.base import BaseModel


class TotNghiep(BaseModel):
    table_name = "tot_nghiep"
    primary_key = "ma_tn"

    @classmethod
    def calculate_xep_loai(cls, gpa: float) -> str:
        """Tính xếp loại tốt nghiệp từ GPA"""
        if gpa >= 3.60:
            return "Xuất sắc"
        elif gpa >= 3.20:
            return "Giỏi"
        elif gpa >= 2.50:
            return "Khá"
        elif gpa >= 2.00:
            return "Trung bình"
        else:
            return "Yếu"

    @classmethod
    def get_or_create(cls, ma_sv: str, gpa: float):
        """Tạo hoặc cập nhật kết quả tốt nghiệp"""
        xep_loai = cls.calculate_xep_loai(gpa)
        return cls.upsert_tot_nghiep(ma_sv, gpa, xep_loai)

    @classmethod
    def upsert_tot_nghiep(cls, ma_sv: str, gpa: float, xep_loai: str):
        """Insert hoặc update kết quả tốt nghiệp"""
        cnx, cursor = cls.get_cursor()
        try:
            cursor.execute(
                "SELECT * FROM tot_nghiep WHERE ma_sv = %s",
                (ma_sv,)
            )
            existing = cursor.fetchone()
            if existing:
                cursor.execute(
                    "UPDATE tot_nghiep SET gpa = %s, xep_loai = %s WHERE ma_sv = %s",
                    (gpa, xep_loai, ma_sv)
                )
            else:
                cursor.execute(
                    "INSERT INTO tot_nghiep (ma_sv, gpa, xep_loai) VALUES (%s, %s, %s)",
                    (ma_sv, gpa, xep_loai)
                )
            cnx.commit()
            return cls.find(ma_sv)
        finally:
            cursor.close()
            cnx.close()

"""
MonHoc Service - Business logic cho MonHoc
"""
from app.models.mon_hoc import MonHoc as MonHocModel
from app.services.base_service import BaseService


class MonHocService(BaseService):
    model = MonHocModel

    @classmethod
    def create_with_validation(cls, ma_mh: str, ten_mh: str, so_tin_chi: int, mo_ta: str = None) -> dict:
        """
        Tạo môn học với validation
        - ma_mh: độ dài tối thiểu 2 ký tự
        - so_tin_chi: > 0
        """
        if len(ma_mh) < 2:
            return {"success": False, "message": "Mã môn học phải có ít nhất 2 ký tự"}

        if so_tin_chi <= 0:
            return {"success": False, "message": "Số tín chỉ phải lớn hơn 0"}

        if cls.model.exists(ma_mh):
            return {"success": False, "message": "Mã môn học đã tồn tại"}

        mon_hoc = cls.model.create({
            "ma_mh": ma_mh,
            "ten_mh": ten_mh,
            "so_tin_chi": so_tin_chi,
            "mo_ta": mo_ta
        })
        return {"success": True, "data": mon_hoc}

"""
ThongBao Service - Business logic cho thông báo
"""
import uuid
from datetime import datetime

from app.models.thong_bao import ThongBao
from app.models.sinh_vien import SinhVien


class ThongBaoService:
    """Service xử lý thông báo"""

    @classmethod
    def create_thong_bao(cls, tieu_de: str, noi_dung: str, ma_admin: str, doi_tuong: str = "all") -> dict:
        """Admin tạo thông báo"""
        # Generate MaTB
        ma_tb = f"TB{uuid.uuid4().hex[:8].upper()}"

        tb = ThongBao.create({
            "ma_tb": ma_tb,
            "tieu_de": tieu_de,
            "noi_dung": noi_dung,
            "nguoi_tao": ma_admin,
            "doi_tuong": doi_tuong
        })

        return {"success": True, "data": tb}

    @classmethod
    def gui_thong_bao_den_sv(cls, ma_tb: str, ma_sv_list: list) -> dict:
        """Gửi thông báo đến danh sách sinh viên"""
        from app.models.base import BaseModel

        created = 0
        errors = []

        for ma_sv in ma_sv_list:
            if not SinhVien.exists(ma_sv):
                errors.append({"ma_sv": ma_sv, "message": "Sinh viên không tồn tại"})
                continue

            try:
                BaseModel.raw_query(
                    """INSERT INTO tb_nguoi_nhan (ma_tb, loai_nguoi_nhan, ma_nguoi_nhan, da_doc)
                       VALUES (%s, 'sinh_vien', %s, 0)""",
                    (ma_tb, ma_sv)
                )
                created += 1
            except Exception as e:
                errors.append({"ma_sv": ma_sv, "message": str(e)})

        return {
            "success": created > 0,
            "created": created,
            "total": len(ma_sv_list),
            "errors": errors
        }

    @classmethod
    def gui_tat_ca_sv(cls, ma_tb: str) -> dict:
        """Gửi thông báo đến tất cả sinh viên"""
        all_sv = SinhVien.all()
        ma_sv_list = [sv["ma_sv"] for sv in all_sv]
        return cls.gui_thong_bao_den_sv(ma_tb, ma_sv_list)

    @classmethod
    def gui_theo_lop(cls, ma_tb: str, ma_lop: str) -> dict:
        """Gửi thông báo đến sinh viên trong lớp"""
        from app.models.lop import Lop
        sv_list = Lop.get_sinh_vien(ma_lop)
        ma_sv_list = [sv["ma_sv"] for sv in sv_list]
        return cls.gui_thong_bao_den_sv(ma_tb, ma_sv_list)

    @classmethod
    def gui_theo_nganh(cls, ma_tb: str, ma_nganh: str) -> dict:
        """Gửi thông báo đến sinh viên trong ngành"""
        from app.models.nganh import Nganh
        lop_list = Nganh.get_lop(ma_nganh)
        ma_sv_list = []
        for lop in lop_list:
            from app.models.lop import Lop
            sv_list = Lop.get_sinh_vien(lop["ma_lop"])
            ma_sv_list.extend([sv["ma_sv"] for sv in sv_list])
        return cls.gui_thong_bao_den_sv(ma_tb, ma_sv_list)

    @classmethod
    def mark_read(cls, ma_tb: str, ma_sv: str) -> dict:
        """Đánh dấu đã đọc"""
        ThongBao.mark_as_read(ma_tb, ma_sv)
        return {"success": True, "message": "Đã đọc"}

    @classmethod
    def get_sv_thong_bao(cls, ma_sv: str) -> dict:
        """Lấy thông báo của sinh viên"""
        if not SinhVien.exists(ma_sv):
            return {"success": False, "message": "Sinh viên không tồn tại"}

        thong_bao_list = SinhVien.get_thong_bao(ma_sv)

        # Count unread
        unread_count = sum(1 for tb in thong_bao_list if not tb.get("da_doc"))

        return {
            "success": True,
            "data": {
                "thong_bao": thong_bao_list,
                "unread_count": unread_count,
                "total": len(thong_bao_list)
            }
        }

    @classmethod
    def delete_thong_bao(cls, ma_tb: str) -> dict:
        """Xóa thông báo"""
        from app.models.base import BaseModel

        # Delete TB_NguoiNhan first (FK)
        BaseModel.raw_query("DELETE FROM tb_nguoi_nhan WHERE ma_tb = %s", (ma_tb,))

        if ThongBao.delete(ma_tb):
            return {"success": True, "message": "Xóa thông báo thành công"}
        return {"success": False, "message": "Thông báo không tồn tại"}

    @classmethod
    def get_all_admin(cls) -> dict:
        """Admin lấy tất cả thông báo"""
        thong_bao_list = ThongBao.get_all_with_creator()
        return {"success": True, "data": thong_bao_list}

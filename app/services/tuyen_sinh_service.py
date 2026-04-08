"""
TuyenSinh Service - Business logic cho tuyển sinh
Quy trình 4 bước:
1. Thí sinh đăng ký tài khoản (AuthService.register_candidate)
2. Thí sinh nộp hồ sơ (hso_xet_tuyen)
3. Admin duyệt → Đậu → auto tạo SinhVien
4. Admin từ chối → Rớt
"""
import random
from datetime import datetime
from werkzeug.security import generate_password_hash

from app.models.hso_xet_tuyen import HSOXetTuyen
from app.models.pt_xet_tuyen import PTXetTuyen
from app.models.sinh_vien import SinhVien
from app.models.tk_xet_tuyen import TKXetTuyen
from app.models.nganh import Nganh
from app.models.lop import Lop


class TuyenSinhService:
    """Service xử lý quy trình tuyển sinh"""

    # ========== Thí sinh nộp hồ sơ ==========

    @classmethod
    def submit_profile(cls, ma_tk: str, ho_ten: str, cccd: str, so_dien_thoai: str) -> dict:
        """
        Thí sinh nộp hồ sơ xét tuyển
        Validation:
        - CCCD: đúng 10 số
        - so_dien_thoai: đúng 10 số
        """
        # Validate CCCD
        if not cccd.isdigit() or len(cccd) != 10:
            return {"success": False, "message": "CCCD phải là 10 chữ số"}

        # Validate so_dien_thoai
        if not so_dien_thoai.isdigit() or len(so_dien_thoai) != 10:
            return {"success": False, "message": "SĐT phải là 10 chữ số"}

        # Check unique CCCD in tk_xet_tuyen
        existing_cccd = TKXetTuyen.raw_query(
            "SELECT * FROM tk_xet_tuyen WHERE cccd = %s",
            (cccd,),
            fetch_one=True
        )
        if existing_cccd:
            return {"success": False, "message": "CCCD đã được sử dụng"}

        # Check unique so_dien_thoai in tk_xet_tuyen
        existing_sdt = TKXetTuyen.raw_query(
            "SELECT * FROM tk_xet_tuyen WHERE so_dien_thoai = %s",
            (so_dien_thoai,),
            fetch_one=True
        )
        if existing_sdt:
            return {"success": False, "message": "SĐT đã được sử dụng"}

        # Update tk_xet_tuyen with profile info
        TKXetTuyen.update(ma_tk, {
            "ho_ten": ho_ten,
            "cccd": cccd,
            "so_dien_thoai": so_dien_thoai
        })

        # Create HSO record
        ma_hs = f"H{random.randint(10000, 99999)}"
        hso = HSOXetTuyen.create({
            "ma_hs": ma_hs,
            "ma_tk": ma_tk,
            "dia_chi": "",
            "truong_thpt": "",
            "nam_tot_nghiep": datetime.now().year
        })

        return {"success": True, "data": hso, "message": "Hồ sơ đã được tạo"}

    @classmethod
    def submit_application(cls, ma_tk: str, ma_nganh: str, phuong_thuc: str, diem: float) -> dict:
        """
        Thí sinh nộp phiếu đăng ký xét tuyển
        Validation:
        - Diem: 0-30
        - MaNganh phải tồn tại
        - Chưa có phiếu đang chờ duyệt cho ngành này
        """
        # Validate Diem
        if diem < 0 or diem > 30:
            return {"success": False, "message": "Điểm phải từ 0 đến 30"}

        # Check MaNganh exists
        if not Nganh.exists(ma_nganh):
            return {"success": False, "message": "Ngành không tồn tại"}

        # Check TK exists
        tk = TKXetTuyen.find(ma_tk)
        if not tk:
            return {"success": False, "message": "Tài khoản không tồn tại"}

        # Check pending application for this major
        pending = PTXetTuyen.raw_query(
            "SELECT * FROM pt_xet_tuyen WHERE ma_tk = %s AND ma_nganh = %s AND trang_thai = 'Cho duyet'",
            (ma_tk, ma_nganh),
            fetch_one=True
        )
        if pending:
            return {"success": False, "message": "Đã có phiếu chờ duyệt cho ngành này"}

        # Generate MaPT
        ma_pt = f"PT{random.randint(1000000000, 9999999999)}"

        # Create PT
        pt = PTXetTuyen.create({
            "ma_pt": ma_pt,
            "ma_tk": ma_tk,
            "ma_nganh": ma_nganh,
            "diem": diem,
            "trang_thai": "Cho duyet",
            "ghi_chu": f"Phương thức: {phuong_thuc}"
        })

        return {"success": True, "data": pt, "message": "Phiếu đăng ký đã được nộp"}

    # ========== Admin duyệt tuyển sinh ==========

    @classmethod
    def approve_application(cls, ma_pt: str, ma_admin: str) -> dict:
        """
        Admin duyệt đậu tuyển sinh
        Auto tạo SinhVien
        """
        pt = PTXetTuyen.find(ma_pt)
        if not pt:
            return {"success": False, "message": "Phiếu không tồn tại"}

        if pt["trang_thai"] != "Cho duyet":
            return {"success": False, "message": "Phiếu đã được xử lý"}

        tk = TKXetTuyen.find(pt["ma_tk"])
        if not tk:
            return {"success": False, "message": "Tài khoản thí sinh không tồn tại"}

        # Update PT status
        PTXetTuyen.update_trang_thai(ma_pt, "Dau", ma_admin)

        # Auto tạo SinhVien
        year = datetime.now().year
        ma_sv = f"SV{year}{random.randint(10000000, 99999999)}"

        # Get first available class for the major
        lop = Lop.raw_query(
            "SELECT ma_lop FROM lop WHERE ma_nganh = %s LIMIT 1",
            (pt["ma_nganh"],),
            fetch_one=True
        )
        ma_lop = lop["ma_lop"] if lop else None

        # Create SinhVien with default password
        sinh_vien = SinhVien.create({
            "ma_sv": ma_sv,
            "ho_ten": tk["ho_ten"],
            "email": f"{ma_sv}@student.edu.vn",
            "mat_khau": generate_password_hash("123456"),
            "ma_lop": ma_lop,
            "cccd": tk["cccd"],
            "so_dien_thoai": tk["so_dien_thoai"]
        })

        return {
            "success": True,
            "message": "Duyệt tuyển thành công",
            "sinh_vien": sinh_vien,
            "ma_sv": ma_sv
        }

    @classmethod
    def reject_application(cls, ma_pt: str, ma_admin: str) -> dict:
        """Admin từ chối tuyển sinh"""
        pt = PTXetTuyen.find(ma_pt)
        if not pt:
            return {"success": False, "message": "Phiếu không tồn tại"}

        if pt["trang_thai"] != "Cho duyet":
            return {"success": False, "message": "Phiếu đã được xử lý"}

        PTXetTuyen.update_trang_thai(ma_pt, "Rot", ma_admin)

        return {"success": True, "message": "Đã từ chối tuyển sinh"}

    # ========== Thí sinh xem trạng thái ==========

    @classmethod
    def get_candidate_status(cls, ma_tk: str) -> dict:
        """Thí sinh xem trạng thái đơn đăng ký"""
        tk = TKXetTuyen.find(ma_tk)
        if not tk:
            return {"success": False, "message": "Chưa có tài khoản"}

        hso = TKXetTuyen.get_ho_so(ma_tk)
        if not hso:
            return {"success": True, "data": {"ho_so": None, "phieu_dang_ky": []}}

        pt_list = HSOXetTuyen.get_phieu_dang_ky(hso["ma_hs"])

        return {
            "success": True,
            "data": {
                "ho_so": hso,
                "phieu_dang_ky": pt_list
            }
        }

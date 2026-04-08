"""
Auth Service - Xử lý đăng nhập cho 3 vai trò
"""
from werkzeug.security import check_password_hash, generate_password_hash

from app.models.quan_tri import QuanTri
from app.models.sinh_vien import SinhVien
from app.models.tk_xet_tuyen import TKXetTuyen
from app.models.hso_xet_tuyen import HSOXetTuyen
from app.middleware.jwt_auth import generate_token


class AuthService:
    """Service xử lý authentication cho 3 vai trò"""

    # ========== Admin Auth ==========

    @staticmethod
    def login_admin(ten_dn: str, mat_khau: str) -> dict:
        """
        Đăng nhập admin
        Returns: {success: bool, token?: str, user?: dict, message?: str}
        """
        admin = QuanTri.find_by_username(ten_dn)
        if not admin:
            return {"success": False, "message": "Tên đăng nhập không tồn tại"}

        # Verify password
        if not check_password_hash(admin["password_hash"], mat_khau):
            return {"success": False, "message": "Mật khẩu không đúng"}

        # Generate token
        token = generate_token({
            "ma_qt": admin["ma_qt"],
            "ho_ten": admin["ho_ten"]
        }, "admin")

        return {
            "success": True,
            "token": token,
            "user": {
                "MaAdmin": admin["ma_qt"],
                "TenDN": admin["ho_ten"],
                "role": "admin"
            }
        }

    # ========== Student Auth ==========

    @staticmethod
    def login_student(ma_sv: str, mat_khau: str) -> dict:
        """
        Đăng nhập sinh viên
        """
        student = SinhVien.find(ma_sv)
        if not student:
            return {"success": False, "message": "Mã sinh viên không tồn tại"}

        if not check_password_hash(student["password_hash"], mat_khau):
            return {"success": False, "message": "Mật khẩu không đúng"}

        token = generate_token({
            "ma_sv": student["ma_sv"],
            "ho_ten": student["ho_ten"],
            "email": student["email"]
        }, "student")

        return {
            "success": True,
            "token": token,
            "user": {
                "MaSV": student["ma_sv"],
                "HoTen": student["ho_ten"],
                "Email": student["email"],
                "role": "student"
            }
        }

    # ========== Candidate Auth ==========

    @staticmethod
    def register_candidate(email: str, mat_khau: str) -> dict:
        """
        Đăng ký tài khoản thí sinh
        Business rules:
        - Email phải có đuôi @gmail.com
        - Email phải unique
        - Password tối thiểu 6 ký tự
        """
        # Validate email format
        if not email.endswith("@gmail.com"):
            return {"success": False, "message": "Email phải có đuôi @gmail.com"}

        # Check email exists
        if TKXetTuyen.find_by_email(email):
            return {"success": False, "message": "Email đã được sử dụng"}

        # Generate MaTK
        import random
        ma_tk = f"TK{random.randint(1000, 9999)}"

        # Create account
        tk = TKXetTuyen.create({
            "ma_tk": ma_tk,
            "email": email,
            "password_hash": generate_password_hash(mat_khau)
        })

        token = generate_token({
            "ma_tk": tk["ma_tk"],
            "email": tk["email"]
        }, "candidate")

        return {
            "success": True,
            "token": token,
            "user": {
                "MaTK": tk["ma_tk"],
                "Email": tk["email"],
                "role": "candidate"
            }
        }

    @staticmethod
    def login_candidate(email: str, mat_khau: str) -> dict:
        """
        Đăng nhập thí sinh
        """
        tk = TKXetTuyen.find_by_email(email)
        if not tk:
            return {"success": False, "message": "Email chưa được đăng ký"}

        if not check_password_hash(tk["password_hash"], mat_khau):
            return {"success": False, "message": "Mật khẩu không đúng"}

        token = generate_token({
            "ma_tk": tk["ma_tk"],
            "email": tk["email"]
        }, "candidate")

        return {
            "success": True,
            "token": token,
            "user": {
                "MaTK": tk["ma_tk"],
                "Email": tk["email"],
                "role": "candidate"
            }
        }

    # ========== Change Password ==========

    @staticmethod
    def change_password(role: str, identifier: str, old_password: str, new_password: str) -> dict:
        """Đổi mật khẩu"""
        if role == "admin":
            user = QuanTri.find_by_username(identifier)
        elif role == "student":
            user = SinhVien.find(identifier)
        else:
            user = TKXetTuyen.find_by_email(identifier)

        if not user:
            return {"success": False, "message": "Người dùng không tồn tại"}

        password_field = "password_hash"
        if role == "admin":
            if not check_password_hash(user["password_hash"], old_password):
                return {"success": False, "message": "Mật khẩu cũ không đúng"}
            QuanTri.update(user["ma_qt"], {"password_hash": generate_password_hash(new_password)})
        elif role == "student":
            if not check_password_hash(user["password_hash"], old_password):
                return {"success": False, "message": "Mật khẩu cũ không đúng"}
            SinhVien.update(user["ma_sv"], {"password_hash": generate_password_hash(new_password)})
        else:
            if not check_password_hash(user["password_hash"], old_password):
                return {"success": False, "message": "Mật khẩu cũ không đúng"}
            TKXetTuyen.update(user["ma_tk"], {"password_hash": generate_password_hash(new_password)})

        return {"success": True, "message": "Đổi mật khẩu thành công"}

"""
Auth Service - Xử lý đăng nhập cho 2 vai trò: admin, student
"""
from werkzeug.security import check_password_hash, generate_password_hash

from app.models.quan_tri import QuanTri
from app.models.sinh_vien import SinhVien
from app.middleware.jwt_auth import generate_token


class AuthService:
    """Service xử lý authentication cho 2 vai trò: admin, student"""

    # ========== Admin Auth ==========

    @staticmethod
    def login_admin(email: str, mat_khau: str) -> dict:
        """
        Đăng nhập admin
        Returns: {success: bool, token?: str, user?: dict, message?: str}
        """
        admin = QuanTri.find_by_username(email)
        if not admin:
            return {"success": False, "message": "Tên đăng nhập không tồn tại"}

        # Verify password — DB uses password_hash column
        if not check_password_hash(admin["password_hash"], mat_khau):
            return {"success": False, "message": "Mật khẩu không đúng"}

        # Generate token — payload keys snake_case for JWT consistency
        token = generate_token({
            "ma_qt": admin["ma_qt"],
            "ho_ten": admin["ho_ten"]
        }, "admin")

        return {
            "success": True,
            "token": token,
            "user": {
                "ma_qt": admin["ma_qt"],
                "ho_ten": admin["ho_ten"],
                "email": admin["email"],
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

        # Verify password — DB uses password_hash column
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
                "ma_sv": student["ma_sv"],
                "ho_ten": student["ho_ten"],
                "email": student["email"],
                "role": "student"
            }
        }

    # ========== Change Password ==========

    @staticmethod
    def change_password(role: str, identifier: str, old_password: str, new_password: str) -> dict:
        """Đổi mật khẩu"""
        if role == "admin":
            user = QuanTri.find_by_username(identifier)
            if not user:
                return {"success": False, "message": "Người dùng không tồn tại"}
            if not check_password_hash(user["password_hash"], old_password):
                return {"success": False, "message": "Mật khẩu cũ không đúng"}
            QuanTri.update_admin(user["ma_qt"], {"password_hash": generate_password_hash(new_password)})
        elif role == "student":
            user = SinhVien.find(identifier)
            if not user:
                return {"success": False, "message": "Người dùng không tồn tại"}
            if not check_password_hash(user["password_hash"], old_password):
                return {"success": False, "message": "Mật khẩu cũ không đúng"}
            SinhVien.update(user["ma_sv"], {"password_hash": generate_password_hash(new_password)})
        else:
            return {"success": False, "message": "Vai trò không hợp lệ"}

        return {"success": True, "message": "Đổi mật khẩu thành công"}

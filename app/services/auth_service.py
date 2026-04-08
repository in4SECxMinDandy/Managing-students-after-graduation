"""
Auth Service - Xử lý đăng nhập cho 2 vai trò: admin, student
"""
import json
import os
from werkzeug.security import check_password_hash, generate_password_hash

from app.models.quan_tri import QuanTri
from app.models.sinh_vien import SinhVien
from app.middleware.jwt_auth import generate_token

_AUTH_DEBUG_LOG = os.path.join(os.path.dirname(os.path.dirname(__file__)), "..", "debug-722d3f.log")


def _dbg_svc(location, message, data, hypothesis_id="ALL"):
    entry = {
        "id": f"log_{id(data)}",
        "sessionId": "722d3f",
        "timestamp": 0,
        "location": location,
        "message": message,
        "data": data,
        "runId": "run1",
        "hypothesisId": hypothesis_id
    }
    try:
        with open(_AUTH_DEBUG_LOG, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    except Exception:
        pass


class AuthService:
    """Service xử lý authentication cho 2 vai trò: admin, student"""

    # ========== Admin Auth ==========

    @staticmethod
    def login_admin(ten_dn: str, mat_khau: str) -> dict:
        """
        Đăng nhập admin
        Returns: {success: bool, token?: str, user?: dict, message?: str}
        """
        _dbg_svc("auth_service.py:login_admin", "ADMIN_LOGIN_START",
                 {"ten_dn": ten_dn, "mat_khau_len": len(mat_khau) if mat_khau else 0},
                 hypothesis_id="ALL")
        admin = QuanTri.find_by_username(ten_dn)
        _dbg_svc("auth_service.py:login_admin", "ADMIN_DB_RESULT",
                 {"found": admin is not None, "keys": list(admin.keys()) if admin else None,
                  "has_password_hash": bool(admin.get("password_hash")) if admin else None},
                 hypothesis_id="H1;H3")
        if not admin:
            return {"success": False, "message": "Tên đăng nhập không tồn tại"}

        # Verify password
        _dbg_svc("auth_service.py:login_admin", "ADMIN_PW_VERIFY",
                 {"db_hash_prefix": admin["password_hash"][:20],
                  "user_input_len": len(mat_khau),
                  "method_used": "werkzeug.check_password_hash"},
                 hypothesis_id="H2;A")
        pw_ok = check_password_hash(admin["password_hash"], mat_khau)
        _dbg_svc("auth_service.py:login_admin", "ADMIN_PW_CHECK",
                 {"password_match": pw_ok},
                 hypothesis_id="H2")
        if not pw_ok:
            return {"success": False, "message": "Mật khẩu không đúng"}

        # Generate token
        token = generate_token({
            "ma_qt": admin["ma_qt"],
            "ho_ten": admin["ho_ten"]
        }, "admin")
        _dbg_svc("auth_service.py:login_admin", "ADMIN_TOKEN_GENERATED",
                 {"token_len": len(token) if token else 0, "ma_qt": admin["ma_qt"]},
                 hypothesis_id="H4")

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
            QuanTri.update(user["ma_qt"], {"password_hash": generate_password_hash(new_password)})
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

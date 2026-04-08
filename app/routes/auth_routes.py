"""
Auth Routes - Authentication endpoints
"""
import json
import os
from flask import Blueprint, request, jsonify

from app.services.auth_service import AuthService

auth_bp = Blueprint("auth", __name__)

_DEBUG_LOG_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "..", "debug-722d3f.log")


def _dbg(location, message, data, hypothesis_id="ALL", run_id="run1"):
    entry = {
        "id": f"log_{json.dumps(data)[:20]}",
        "sessionId": "722d3f",
        "timestamp": 0,
        "location": location,
        "message": message,
        "data": data,
        "runId": run_id,
        "hypothesisId": hypothesis_id
    }
    try:
        with open(_DEBUG_LOG_PATH, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    except Exception:
        pass


@auth_bp.route("/login", methods=["POST"])
def login():
    """
    Đăng nhập - tự động detect role
    Body: {ten_dn, mat_khau, role}
    """
    data = request.get_json()
    role = data.get("role", "")
    _dbg("auth_routes.py:login", "LOGIN_ATTEMPT",
         {"role": role, "ten_dn": data.get("ten_dn") or data.get("ma_sv")},
         hypothesis_id="ALL")
    if role == "admin":
        result = AuthService.login_admin(data.get("ten_dn"), data.get("mat_khau"))
    elif role == "student":
        result = AuthService.login_student(data.get("ma_sv"), data.get("mat_khau"))
    else:
        _dbg("auth_routes.py:login", "NO_VALID_ROLE", {"role": role}, hypothesis_id="H_UNK")
        return jsonify({"error": "Bad Request", "message": "Vui lòng chọn vai trò (admin hoặc student)"}), 400

    _dbg("auth_routes.py:login", "LOGIN_RESULT",
         {"success": result["success"], "message": result.get("message"), "role": role},
         hypothesis_id="ALL")
    if result["success"]:
        return jsonify(result)
    return jsonify({"error": "Unauthorized", "message": result["message"]}), 401


@auth_bp.route("/change-password", methods=["POST"])
def change_password():
    """
    Đổi mật khẩu
    Body: {role, identifier, old_password, new_password}
    """
    data = request.get_json()
    result = AuthService.change_password(
        data.get("role"),
        data.get("identifier"),
        data.get("old_password"),
        data.get("new_password")
    )

    if result["success"]:
        return jsonify(result)
    return jsonify({"error": "Bad Request", "message": result["message"]}), 400


@auth_bp.route("/me", methods=["GET"])
def me():
    """Lấy thông tin user hiện tại (requires JWT)"""
    from app.middleware.jwt_auth import jwt_required

    @jwt_required
    def get_user():
        from flask import g
        return jsonify(g.current_user)

    return get_user()

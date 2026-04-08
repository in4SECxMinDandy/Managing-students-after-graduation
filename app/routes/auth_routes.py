"""
Auth Routes - Authentication endpoints
"""
from flask import Blueprint, request, jsonify

from app.services.auth_service import AuthService

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["POST"])
def login():
    """
    Đăng nhập - tự động detect role
    Body: {ten_dn, mat_khau, role}
    """
    data = request.get_json()
    role = data.get("role", "")

    if role == "admin":
        result = AuthService.login_admin(data.get("ten_dn"), data.get("mat_khau"))
    elif role == "student":
        result = AuthService.login_student(data.get("ma_sv"), data.get("mat_khau"))
    elif role == "candidate":
        result = AuthService.login_candidate(data.get("email"), data.get("mat_khau"))
    else:
        return jsonify({"error": "Bad Request", "message": "Vui lòng chọn vai trò"}), 400

    if result["success"]:
        return jsonify(result)
    return jsonify({"error": "Unauthorized", "message": result["message"]}), 401


@auth_bp.route("/register-candidate", methods=["POST"])
def register_candidate():
    """
    Đăng ký tài khoản thí sinh
    Body: {email, mat_khau}
    """
    data = request.get_json()
    email = data.get("email", "")
    mat_khau = data.get("mat_khau", "")

    if not mat_khau or len(mat_khau) < 6:
        return jsonify({"error": "Bad Request", "message": "Mật khẩu phải tối thiểu 6 ký tự"}), 400

    result = AuthService.register_candidate(email, mat_khau)

    if result["success"]:
        return jsonify(result), 201
    return jsonify({"error": "Bad Request", "message": result["message"]}), 400


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

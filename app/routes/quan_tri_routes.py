"""
QuanTri Routes - CRUD endpoints cho QuanTri (Admin accounts)
"""
from flask import Blueprint, request, jsonify, g

from app.models.quan_tri import QuanTri
from app.middleware.jwt_auth import admin_required
from werkzeug.security import generate_password_hash

quan_tri_bp = Blueprint("quan_tri", __name__)


@quan_tri_bp.route("/", methods=["GET"])
@admin_required
def index():
    """Lấy danh sách tất cả admin"""
    admins = QuanTri.get_all_admins(order_by="ma_qt")
    # Strip password hash from response
    clean_admins = [{k: v for k, v in a.items() if k != "password_hash"} for a in admins]
    return jsonify({"success": True, "data": clean_admins})


@quan_tri_bp.route("/<ma_qt>", methods=["GET"])
@admin_required
def show(ma_qt):
    """Lấy thông tin một admin"""
    admin = QuanTri.get_by_id(ma_qt)
    if not admin:
        return jsonify({"error": "Not Found", "message": "Admin không tồn tại"}), 404
    clean = {k: v for k, v in admin.items() if k != "password_hash"}
    return jsonify({"success": True, "data": clean})


@quan_tri_bp.route("/", methods=["POST"])
@admin_required
def create():
    """Tạo admin mới"""
    data = request.get_json()

    # Validate required fields
    required = ["ma_qt", "ho_ten", "email", "password_hash"]
    for field in required:
        if not data.get(field):
            return jsonify({"error": "Bad Request", "message": f"Thiếu trường: {field}"}), 400

    # Check if ma_qt already exists
    if QuanTri.exists(data["ma_qt"]):
        return jsonify({"error": "Bad Request", "message": "Mã admin đã tồn tại"}), 400

    # Check if email already taken
    existing = QuanTri.find_by_username(data["email"])
    if existing:
        return jsonify({"error": "Bad Request", "message": "Email đã được sử dụng"}), 400

    # Create with hashed password
    admin = QuanTri.create_admin({
        "ma_qt": data["ma_qt"],
        "ho_ten": data["ho_ten"],
        "email": data["email"],
        "password_hash": generate_password_hash(data["password_hash"])
    })

    clean = {k: v for k, v in admin.items() if k != "password_hash"}
    return jsonify({"success": True, "data": clean}), 201


@quan_tri_bp.route("/<ma_qt>", methods=["PUT"])
@admin_required
def update(ma_qt):
    """Cập nhật thông tin admin"""
    data = request.get_json()

    # Check admin exists
    existing = QuanTri.get_by_id(ma_qt)
    if not existing:
        return jsonify({"error": "Not Found", "message": "Admin không tồn tại"}), 404

    update_data = {}
    if data.get("ho_ten"):
        update_data["ho_ten"] = data["ho_ten"]
    if data.get("email"):
        # Check email uniqueness (exclude current admin)
        other = QuanTri.find_by_username(data["email"])
        if other and other["ma_qt"] != ma_qt:
            return jsonify({"error": "Bad Request", "message": "Email đã được sử dụng"}), 400
        update_data["email"] = data["email"]
    if data.get("password_hash"):
        # Only update password if provided
        update_data["password_hash"] = generate_password_hash(data["password_hash"])

    if not update_data:
        return jsonify({"error": "Bad Request", "message": "Không có thông tin để cập nhật"}), 400

    updated = QuanTri.update_admin(ma_qt, update_data)
    clean = {k: v for k, v in updated.items() if k != "password_hash"}
    return jsonify({"success": True, "data": clean})


@quan_tri_bp.route("/<ma_qt>", methods=["DELETE"])
@admin_required
def delete(ma_qt):
    """Xóa admin"""
    # Prevent deleting yourself
    if g.current_user.get("ma_qt") == ma_qt:
        return jsonify({"error": "Bad Request", "message": "Không thể xóa tài khoản đang đăng nhập"}), 400

    if QuanTri.delete_admin(ma_qt):
        return jsonify({"success": True, "message": "Xóa admin thành công"})
    return jsonify({"error": "Not Found", "message": "Admin không tồn tại"}), 404

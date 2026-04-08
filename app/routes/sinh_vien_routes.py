"""
SinhVien Routes - Endpoints cho SinhVien
"""
from flask import Blueprint, request, jsonify, g

from app.services.sinh_vien_service import SinhVienService
from app.middleware.jwt_auth import admin_required, student_required, admin_or_student

sinh_vien_bp = Blueprint("sinh_vien", __name__)


@sinh_vien_bp.route("/", methods=["GET"])
@admin_required
def index():
    """Admin: Lấy danh sách sinh viên"""
    from app.models.sinh_vien import SinhVien
    sinh_viens = SinhVien.all(order_by="ma_sv")
    return jsonify({"success": True, "data": sinh_viens})


@sinh_vien_bp.route("/<ma_sv>", methods=["GET"])
@admin_or_student
def show(ma_sv):
    """Lấy thông tin sinh viên"""
    # Students can only view their own profile
    if g.role == "student" and g.current_user["ma_sv"] != ma_sv:
        return jsonify({"error": "Forbidden", "message": "Không có quyền xem thông tin này"}), 403

    result = SinhVienService.get_profile_with_details(ma_sv)
    if result["success"]:
        return jsonify(result)
    return jsonify({"error": "Not Found", "message": result["message"]}), 404


@sinh_vien_bp.route("/", methods=["POST"])
@admin_required
def create():
    """Admin: Tạo sinh viên mới"""
    data = request.get_json()
    result = SinhVienService.create_with_validation(
        data.get("ma_sv"),
        data.get("ho_ten"),
        data.get("ngay_sinh"),
        data.get("email"),
        data.get("mat_khau"),
        data.get("ma_lop"),
        data.get("cccd"),
        data.get("so_dien_thoai")
    )
    if result["success"]:
        return jsonify(result), 201
    return jsonify({"error": "Bad Request", "message": result["message"]}), 400


@sinh_vien_bp.route("/<ma_sv>", methods=["PUT"])
@admin_or_student
def update(ma_sv):
    """Cập nhật thông tin sinh viên"""
    if g.role == "student" and g.current_user["ma_sv"] != ma_sv:
        return jsonify({"error": "Forbidden", "message": "Không có quyền sửa thông tin này"}), 403

    data = request.get_json()
    result = SinhVienService.update_profile(ma_sv, data)

    if result["success"]:
        return jsonify(result)
    return jsonify({"error": "Bad Request", "message": result["message"]}), 400


@sinh_vien_bp.route("/<ma_sv>", methods=["DELETE"])
@admin_required
def delete(ma_sv):
    """Admin: Xóa sinh viên"""
    from app.models.sinh_vien import SinhVien
    if SinhVien.delete(ma_sv):
        return jsonify({"success": True, "message": "Xóa sinh viên thành công"})
    return jsonify({"error": "Not Found", "message": "Sinh viên không tồn tại"}), 404


@sinh_vien_bp.route("/search", methods=["GET"])
@admin_required
def search():
    """Admin: Tìm kiếm sinh viên"""
    keyword = request.args.get("q", "")
    if not keyword:
        return jsonify({"success": True, "data": []})

    from app.models.sinh_vien import SinhVien
    results = SinhVien.raw_query("""
        SELECT * FROM sinh_vien
        WHERE ma_sv LIKE %s OR ho_ten LIKE %s OR email LIKE %s
        LIMIT 20
    """, (f"%{keyword}%", f"%{keyword}%", f"%{keyword}%"))

    return jsonify({"success": True, "data": results})

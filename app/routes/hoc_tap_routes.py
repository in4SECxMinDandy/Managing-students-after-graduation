"""
HocTap Routes - Endpoints cho Kết quả học tập
"""
from flask import Blueprint, request, jsonify, g

from app.services.hoc_tap_service import HocTapService
from app.middleware.jwt_auth import admin_required, student_required, admin_or_student

hoc_tap_bp = Blueprint("hoc_tap", __name__)


@hoc_tap_bp.route("/diem/<ma_sv>", methods=["GET"])
@admin_or_student
def get_bang_diem(ma_sv):
    """Lấy bảng điểm của sinh viên"""
    if g.role == "student" and g.current_user["ma_sv"] != ma_sv:
        return jsonify({"error": "Forbidden", "message": "Không có quyền"}), 403

    result = HocTapService.get_bang_diem(ma_sv)
    if result["success"]:
        return jsonify(result)
    return jsonify({"error": "Not Found", "message": result["message"]}), 404


@hoc_tap_bp.route("/diem", methods=["POST"])
@admin_required
def nhap_diem():
    """Admin: Nhập điểm cho sinh viên"""
    data = request.get_json()
    result = HocTapService.nhap_diem(
        data.get("ma_sv"),
        data.get("ma_mh"),
        data.get("diem")
    )
    if result["success"]:
        return jsonify(result), 201
    return jsonify({"error": "Bad Request", "message": result["message"]}), 400


@hoc_tap_bp.route("/diem/batch", methods=["POST"])
@admin_required
def nhap_nhieu_diem():
    """Admin: Nhập nhiều điểm cùng lúc"""
    data = request.get_json()
    result = HocTapService.nhap_nhieu_diem(data.get("diem_list", []))
    return jsonify(result)


@hoc_tap_bp.route("/diem/<ma_sv>/<ma_mh>", methods=["DELETE"])
@admin_required
def xoa_diem(ma_sv, ma_mh):
    """Admin: Xóa điểm"""
    result = HocTapService.delete_diem(ma_sv, ma_mh)
    if result["success"]:
        return jsonify(result)
    return jsonify({"error": "Not Found", "message": result["message"]}), 404


@hoc_tap_bp.route("/gpa/<ma_sv>", methods=["GET"])
@admin_or_student
def get_gpa(ma_sv):
    """Tính GPA của sinh viên"""
    if g.role == "student" and g.current_user["ma_sv"] != ma_sv:
        return jsonify({"error": "Forbidden", "message": "Không có quyền"}), 403

    result = HocTapService.calculate_gpa(ma_sv)
    if result["success"]:
        return jsonify(result)
    return jsonify({"error": "Not Found", "message": result["message"]}), 404


@hoc_tap_bp.route("/mon-hoc", methods=["GET"])
def get_mon_hoc():
    """Lấy danh sách môn học"""
    from app.models.mon_hoc import MonHoc
    mon_hocs = MonHoc.all(order_by="ma_mh")
    return jsonify({"success": True, "data": mon_hocs})

"""
TotNghiep Routes - Endpoints cho tốt nghiệp
"""
from flask import Blueprint, request, jsonify, g

from app.services.tot_nghiep_service import TotNghiepService
from app.middleware.jwt_auth import admin_required, student_required, admin_or_student

tot_nghiep_bp = Blueprint("tot_nghiep", __name__)


@tot_nghiep_bp.route("/check/<ma_sv>", methods=["GET"])
@admin_or_student
def check(ma_sv):
    """Xét tốt nghiệp cho sinh viên"""
    if g.role == "student" and g.current_user["ma_sv"] != ma_sv:
        return jsonify({"error": "Forbidden", "message": "Không có quyền"}), 403

    result = TotNghiepService.check_graduation(ma_sv)
    if result["success"]:
        return jsonify(result)
    return jsonify({"error": "Not Found", "message": result["message"]}), 404


@tot_nghiep_bp.route("/status/<ma_sv>", methods=["GET"])
@admin_or_student
def status(ma_sv):
    """Lấy trạng thái tốt nghiệp hiện tại"""
    if g.role == "student" and g.current_user["ma_sv"] != ma_sv:
        return jsonify({"error": "Forbidden", "message": "Không có quyền"}), 403

    result = TotNghiepService.get_graduation_status(ma_sv)
    if result["success"]:
        return jsonify(result)
    return jsonify({"error": "Not Found", "message": result["message"]}), 404


@tot_nghiep_bp.route("/all", methods=["GET"])
@admin_required
def get_all():
    """Admin: Lấy danh sách tốt nghiệp"""
    from app.models.tot_nghiep import TotNghiep
    tn_list = TotNghiep.raw_query("""
        SELECT tn.*, sv.ho_ten, sv.email, l.ten_lop
        FROM tot_nghiep tn
        INNER JOIN sinh_vien sv ON tn.ma_sv = sv.ma_sv
        LEFT JOIN lop l ON sv.ma_lop = l.ma_lop
        ORDER BY tn.gpa DESC
    """)
    return jsonify({"success": True, "data": tn_list})


@tot_nghiep_bp.route("/xep-loai-stats", methods=["GET"])
@admin_required
def xep_loai_stats():
    """Admin: Thống kê xếp loại tốt nghiệp"""
    from app.models.tot_nghiep import TotNghiep
    stats = TotNghiep.raw_query("""
        SELECT xep_loai, COUNT(*) as so_luong
        FROM tot_nghiep
        GROUP BY xep_loai
        ORDER BY so_luong DESC
    """)
    return jsonify({"success": True, "data": stats})

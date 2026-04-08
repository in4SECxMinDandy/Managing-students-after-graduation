"""
TuyenSinh Routes - Endpoints cho tuyển sinh
"""
from flask import Blueprint, request, jsonify, g

from app.services.tuyen_sinh_service import TuyenSinhService
from app.middleware.jwt_auth import admin_required, candidate_required, jwt_required

tuyen_sinh_bp = Blueprint("tuyen_sinh", __name__)


@tuyen_sinh_bp.route("/submit-profile", methods=["POST"])
@candidate_required
def submit_profile():
    """
    Thí sinh nộp hồ sơ
    Body: {ho_ten, cccd, so_dien_thoai}
    """
    data = request.get_json()
    ma_tk = g.current_user["ma_tk"]

    result = TuyenSinhService.submit_profile(
        ma_tk,
        data.get("ho_ten"),
        data.get("cccd"),
        data.get("so_dien_thoai")
    )

    if result["success"]:
        return jsonify(result), 201
    return jsonify({"error": "Bad Request", "message": result["message"]}), 400


@tuyen_sinh_bp.route("/submit-application", methods=["POST"])
@candidate_required
def submit_application():
    """
    Thí sinh nộp phiếu đăng ký xét tuyển
    Body: {ma_nganh, phuong_thuc, diem}
    """
    data = request.get_json()
    ma_tk = g.current_user["ma_tk"]

    result = TuyenSinhService.submit_application(
        ma_tk,
        data.get("ma_nganh"),
        data.get("phuong_thuc"),
        data.get("diem")
    )

    if result["success"]:
        return jsonify(result), 201
    return jsonify({"error": "Bad Request", "message": result["message"]}), 400


@tuyen_sinh_bp.route("/status", methods=["GET"])
@candidate_required
def get_status():
    """Thí sinh xem trạng thái đơn"""
    ma_tk = g.current_user["ma_tk"]
    result = TuyenSinhService.get_candidate_status(ma_tk)

    if result["success"]:
        return jsonify(result)
    return jsonify({"error": "Not Found", "message": result["message"]}), 404


# ========== Admin Endpoints ==========

@tuyen_sinh_bp.route("/pending", methods=["GET"])
@admin_required
def get_pending():
    """Admin: Lấy danh sách phiếu chờ duyệt"""
    from app.models.pt_xet_tuyen import PTXetTuyen
    pt_list = PTXetTuyen.get_all_with_details()
    # Filter chỉ lấy chờ duyệt
    pending = [pt for pt in pt_list if pt["trang_thai"] == "Cho duyet"]
    return jsonify({"success": True, "data": pending})


@tuyen_sinh_bp.route("/all", methods=["GET"])
@admin_required
def get_all():
    """Admin: Lấy tất cả phiếu xét tuyển"""
    from app.models.pt_xet_tuyen import PTXetTuyen
    pt_list = PTXetTuyen.get_all_with_details()
    return jsonify({"success": True, "data": pt_list})


@tuyen_sinh_bp.route("/approve/<ma_pt>", methods=["POST"])
@admin_required
def approve(ma_pt):
    """Admin duyệt đậu tuyển sinh"""
    ma_admin = g.current_user["ma_qt"]
    result = TuyenSinhService.approve_application(ma_pt, ma_admin)

    if result["success"]:
        return jsonify(result)
    return jsonify({"error": "Bad Request", "message": result["message"]}), 400


@tuyen_sinh_bp.route("/reject/<ma_pt>", methods=["POST"])
@admin_required
def reject(ma_pt):
    """Admin từ chối tuyển sinh"""
    ma_admin = g.current_user["ma_qt"]
    result = TuyenSinhService.reject_application(ma_pt, ma_admin)

    if result["success"]:
        return jsonify(result)
    return jsonify({"error": "Bad Request", "message": result["message"]}), 400


@tuyen_sinh_bp.route("/approve-all", methods=["POST"])
@admin_required
def approve_all():
    """Admin duyệt tất cả phiếu chờ duyệt"""
    from app.models.pt_xet_tuyen import PTXetTuyen
    ma_admin = g.current_user["ma_qt"]

    pending = PTXetTuyen.get_cho_duyet()
    approved = []
    errors = []

    for pt in pending:
        result = TuyenSinhService.approve_application(pt["ma_pt"], ma_admin)
        if result["success"]:
            approved.append(result.get("ma_sv"))
        else:
            errors.append({"ma_pt": pt["ma_pt"], "message": result["message"]})

    return jsonify({
        "success": True,
        "approved": len(approved),
        "errors": len(errors),
        "ma_sv_list": approved,
        "error_details": errors
    })

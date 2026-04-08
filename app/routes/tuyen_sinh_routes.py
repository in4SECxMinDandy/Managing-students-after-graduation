"""
TuyenSinh Routes - Endpoints cho tuyển sinh
- Public: Nop ho so, nop phieu, xem trang thai (khong can dang nhap)
- Admin: Duyet, tu choi, xem danh sach
"""
from flask import Blueprint, request, jsonify, g

from app.services.tuyen_sinh_service import TuyenSinhService
from app.middleware.jwt_auth import admin_required

tuyen_sinh_bp = Blueprint("tuyen_sinh", __name__)


# ========== Public Endpoints (khong can dang nhap) ==========

@tuyen_sinh_bp.route("/submit-profile", methods=["POST"])
def submit_profile():
    """
    Nop ho so xet tuyen (khong can dang nhap)
    Body: {ho_ten, cccd, so_dien_thoai}
    """
    data = request.get_json()

    result = TuyenSinhService.submit_profile(
        data.get("ho_ten"),
        data.get("cccd"),
        data.get("so_dien_thoai")
    )

    if result["success"]:
        return jsonify(result), 201
    return jsonify({"error": "Bad Request", "message": result["message"]}), 400


@tuyen_sinh_bp.route("/submit-application", methods=["POST"])
def submit_application():
    """
    Nop phieu dang ky xet tuyen (khong can dang nhap)
    Body: {ma_hs, ma_nganh, phuong_thuc, diem}
    """
    data = request.get_json()

    result = TuyenSinhService.submit_application(
        data.get("ma_hs"),
        data.get("ma_nganh"),
        data.get("phuong_thuc"),
        data.get("diem")
    )

    if result["success"]:
        return jsonify(result), 201
    return jsonify({"error": "Bad Request", "message": result["message"]}), 400


@tuyen_sinh_bp.route("/status/<ma_hs>", methods=["GET"])
def get_status(ma_hs):
    """Xem trang thai ho so (khong can dang nhap)"""
    result = TuyenSinhService.get_profile_status(ma_hs)

    if result["success"]:
        return jsonify(result)
    return jsonify({"error": "Not Found", "message": result["message"]}), 404


# ========== Admin Endpoints ==========

@tuyen_sinh_bp.route("/pending", methods=["GET"])
@admin_required
def get_pending():
    """Admin: Lay danh sach phieu cho duyet"""
    from app.models.pt_xet_tuyen import PTXetTuyen
    pt_list = PTXetTuyen.get_all_with_details()
    # Filter chi lay cho duyet
    pending = [pt for pt in pt_list if pt["trang_thai"] == "Cho duyet"]
    return jsonify({"success": True, "data": pending})


@tuyen_sinh_bp.route("/all", methods=["GET"])
@admin_required
def get_all():
    """Admin: Lay tat ca phieu xet tuyen"""
    from app.models.pt_xet_tuyen import PTXetTuyen
    pt_list = PTXetTuyen.get_all_with_details()
    return jsonify({"success": True, "data": pt_list})


@tuyen_sinh_bp.route("/approve/<ma_pt>", methods=["POST"])
@admin_required
def approve(ma_pt):
    """Admin duyet dau tuyen sinh"""
    ma_admin = g.current_user["ma_qt"]
    result = TuyenSinhService.approve_application(ma_pt, ma_admin)

    if result["success"]:
        return jsonify(result)
    return jsonify({"error": "Bad Request", "message": result["message"]}), 400


@tuyen_sinh_bp.route("/reject/<ma_pt>", methods=["POST"])
@admin_required
def reject(ma_pt):
    """Admin tu choi tuyen sinh"""
    ma_admin = g.current_user["ma_qt"]
    result = TuyenSinhService.reject_application(ma_pt, ma_admin)

    if result["success"]:
        return jsonify(result)
    return jsonify({"error": "Bad Request", "message": result["message"]}), 400


@tuyen_sinh_bp.route("/approve-all", methods=["POST"])
@admin_required
def approve_all():
    """Admin duyet tat ca phieu cho duyet"""
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

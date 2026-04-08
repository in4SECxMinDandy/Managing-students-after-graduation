"""
ThongBao Routes - Endpoints cho thông báo
"""
from flask import Blueprint, request, jsonify, g

from app.services.thong_bao_service import ThongBaoService
from app.middleware.jwt_auth import admin_required, student_required, admin_or_student

thong_bao_bp = Blueprint("thong_bao", __name__)


# ========== Student Endpoints ==========

@thong_bao_bp.route("/my", methods=["GET"])
@student_required
def get_my_thong_bao():
    """Sinh viên: Lấy thông báo của mình"""
    ma_sv = g.current_user["ma_sv"]
    result = ThongBaoService.get_sv_thong_bao(ma_sv)
    return jsonify(result)


@thong_bao_bp.route("/read/<ma_tb>", methods=["POST"])
@student_required
def mark_read(ma_tb):
    """Sinh viên: Đánh dấu đã đọc"""
    ma_sv = g.current_user["ma_sv"]
    result = ThongBaoService.mark_read(ma_tb, ma_sv)
    return jsonify(result)


# ========== Admin Endpoints ==========

@thong_bao_bp.route("/", methods=["GET"])
@admin_required
def get_all():
    """Admin: Lấy tất cả thông báo"""
    result = ThongBaoService.get_all_admin()
    return jsonify(result)


@thong_bao_bp.route("/", methods=["POST"])
@admin_required
def create():
    """Admin: Tạo thông báo"""
    data = request.get_json()
    tieu_de = data.get("tieu_de", "")
    noi_dung = data.get("noi_dung", "")

    if not noi_dung:
        return jsonify({"error": "Bad Request", "message": "Nội dung không được trống"}), 400

    ma_admin = g.current_user["ma_qt"]

    # Tạo thông báo
    result = ThongBaoService.create_thong_bao(tieu_de, noi_dung, ma_admin)

    if not result["success"]:
        return jsonify({"error": "Bad Request", "message": "Tạo thông báo thất bại"}), 400

    ma_tb = result["data"]["ma_tb"]

    # Gửi đến đối tượng được chọn
    gui_den = data.get("gui_den", "all")  # "all" | "lop" | "nganh"
    ma_target = data.get("ma_target")  # ma_lop hoặc ma_nganh

    if gui_den == "all":
        send_result = ThongBaoService.gui_tat_ca_sv(ma_tb)
    elif gui_den == "lop":
        if not ma_target:
            return jsonify({"error": "Bad Request", "message": "Thiếu mã lớp"}), 400
        send_result = ThongBaoService.gui_theo_lop(ma_tb, ma_target)
    elif gui_den == "nganh":
        if not ma_target:
            return jsonify({"error": "Bad Request", "message": "Thiếu mã ngành"}), 400
        send_result = ThongBaoService.gui_theo_nganh(ma_tb, ma_target)
    else:
        send_result = {"created": 0}

    return jsonify({
        "success": True,
        "thong_bao": result["data"],
        "send_result": send_result
    }), 201


@thong_bao_bp.route("/<ma_tb>", methods=["DELETE"])
@admin_required
def delete(ma_tb):
    """Admin: Xóa thông báo"""
    result = ThongBaoService.delete_thong_bao(ma_tb)
    if result["success"]:
        return jsonify(result)
    return jsonify({"error": "Not Found", "message": result["message"]}), 404


@thong_bao_bp.route("/<ma_tb>/details", methods=["GET"])
@admin_required
def details(ma_tb):
    """Admin: Chi tiết thông báo và danh sách người nhận"""
    from app.models.thong_bao import ThongBao

    tb = ThongBao.find(ma_tb)
    if not tb:
        return jsonify({"error": "Not Found", "message": "Thông báo không tồn tại"}), 404

    nguoi_nhan = ThongBao.get_nguoi_nhan(ma_tb)
    unread = [n for n in nguoi_nhan if not n.get("da_doc")]

    return jsonify({
        "success": True,
        "data": {
            "thong_bao": tb,
            "nguoi_nhan": nguoi_nhan,
            "total": len(nguoi_nhan),
            "da_doc": len(nguoi_nhan) - len(unread),
            "chua_doc": len(unread)
        }
    })

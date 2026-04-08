"""
MonHoc Routes - CRUD endpoints cho MonHoc
"""
from flask import Blueprint, request, jsonify

from app.services.mon_hoc_service import MonHocService
from app.middleware.jwt_auth import admin_required

mon_hoc_bp = Blueprint("mon_hoc", __name__)


@mon_hoc_bp.route("/", methods=["GET"])
def index():
    """Lấy danh sách môn học"""
    mon_hocs = MonHocService.get_all(order_by="ma_mh")
    return jsonify({"success": True, "data": mon_hocs})


@mon_hoc_bp.route("/<ma_mh>", methods=["GET"])
def show(ma_mh):
    """Lấy thông tin môn học"""
    mon_hoc = MonHocService.get_by_id(ma_mh)
    if not mon_hoc:
        return jsonify({"error": "Not Found", "message": "Môn học không tồn tại"}), 404
    return jsonify({"success": True, "data": mon_hoc})


@mon_hoc_bp.route("/", methods=["POST"])
@admin_required
def create():
    """Tạo môn học mới"""
    data = request.get_json()
    result = MonHocService.create_with_validation(
        data.get("ma_mh"),
        data.get("ten_mh"),
        data.get("so_tin_chi", 0),
        data.get("mo_ta")
    )
    if result["success"]:
        return jsonify(result), 201
    return jsonify({"error": "Bad Request", "message": result["message"]}), 400


@mon_hoc_bp.route("/<ma_mh>", methods=["PUT"])
@admin_required
def update(ma_mh):
    """Cập nhật môn học"""
    data = request.get_json()
    update_data = {}
    if "ten_mh" in data:
        update_data["ten_mh"] = data["ten_mh"]
    if "so_tin_chi" in data:
        update_data["so_tin_chi"] = data["so_tin_chi"]
    if "mo_ta" in data:
        update_data["mo_ta"] = data["mo_ta"]

    mon_hoc = MonHocService.update(ma_mh, update_data)
    if mon_hoc:
        return jsonify({"success": True, "data": mon_hoc})
    return jsonify({"error": "Not Found", "message": "Môn học không tồn tại"}), 404


@mon_hoc_bp.route("/<ma_mh>", methods=["DELETE"])
@admin_required
def delete(ma_mh):
    """Xóa môn học"""
    if MonHocService.delete(ma_mh):
        return jsonify({"success": True, "message": "Xóa môn học thành công"})
    return jsonify({"error": "Not Found", "message": "Môn học không tồn tại"}), 404

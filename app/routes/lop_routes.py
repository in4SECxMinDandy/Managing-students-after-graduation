"""
Lop Routes - CRUD endpoints cho Lop
"""
from flask import Blueprint, request, jsonify

from app.services.lop_service import LopService
from app.middleware.jwt_auth import admin_required

lop_bp = Blueprint("lop", __name__)


@lop_bp.route("/", methods=["GET"])
def index():
    """Lấy danh sách lớp"""
    lops = LopService.get_all(order_by="ma_lop")
    return jsonify({"success": True, "data": lops})


@lop_bp.route("/<ma_lop>", methods=["GET"])
def show(ma_lop):
    """Lấy thông tin lớp"""
    lop = LopService.get_by_id(ma_lop)
    if not lop:
        return jsonify({"error": "Not Found", "message": "Lớp không tồn tại"}), 404
    return jsonify({"success": True, "data": lop})


@lop_bp.route("/", methods=["POST"])
@admin_required
def create():
    """Tạo lớp mới"""
    data = request.get_json()
    result = LopService.create_with_validation(
        data.get("ma_lop"),
        data.get("ten_lop"),
        data.get("ma_nganh"),
        data.get("khoa_hoc")
    )
    if result["success"]:
        return jsonify(result), 201
    return jsonify({"error": "Bad Request", "message": result["message"]}), 400


@lop_bp.route("/<ma_lop>", methods=["PUT"])
@admin_required
def update(ma_lop):
    """Cập nhật lớp"""
    data = request.get_json()
    update_data = {}
    if "ten_lop" in data:
        update_data["ten_lop"] = data["ten_lop"]
    if "ma_nganh" in data:
        update_data["ma_nganh"] = data["ma_nganh"]
    if "khoa_hoc" in data:
        update_data["khoa_hoc"] = data["khoa_hoc"]

    lop = LopService.update(ma_lop, update_data)
    if lop:
        return jsonify({"success": True, "data": lop})
    return jsonify({"error": "Not Found", "message": "Lớp không tồn tại"}), 404


@lop_bp.route("/<ma_lop>", methods=["DELETE"])
@admin_required
def delete(ma_lop):
    """Xóa lớp"""
    if LopService.delete(ma_lop):
        return jsonify({"success": True, "message": "Xóa lớp thành công"})
    return jsonify({"error": "Not Found", "message": "Lớp không tồn tại"}), 404


@lop_bp.route("/<ma_lop>/sinh-vien", methods=["GET"])
def get_sinh_vien(ma_lop):
    """Lấy danh sách sinh viên thuộc lớp"""
    result = LopService.get_sinh_vien_by_lop(ma_lop)
    if result["success"]:
        return jsonify(result)
    return jsonify({"error": "Not Found", "message": result["message"]}), 404

"""
Nganh Routes - CRUD endpoints cho Nganh
"""
from flask import Blueprint, request, jsonify

from app.services.nganh_service import NganhService
from app.middleware.jwt_auth import admin_required

nganh_bp = Blueprint("nganh", __name__)


@nganh_bp.route("/", methods=["GET"])
def index():
    """Lấy danh sách ngành"""
    nganhs = NganhService.get_all(order_by="ma_nganh")
    return jsonify({"success": True, "data": nganhs})


@nganh_bp.route("/<ma_nganh>", methods=["GET"])
def show(ma_nganh):
    """Lấy thông tin ngành"""
    nganh = NganhService.get_by_id(ma_nganh)
    if not nganh:
        return jsonify({"error": "Not Found", "message": "Ngành không tồn tại"}), 404
    return jsonify({"success": True, "data": nganh})


@nganh_bp.route("/", methods=["POST"])
@admin_required
def create():
    """Tạo ngành mới"""
    data = request.get_json()
    result = NganhService.create_with_validation(
        data.get("ma_nganh"),
        data.get("ten_nganh"),
        data.get("ma_khoa")
    )
    if result["success"]:
        return jsonify(result), 201
    return jsonify({"error": "Bad Request", "message": result["message"]}), 400


@nganh_bp.route("/<ma_nganh>", methods=["PUT"])
@admin_required
def update(ma_nganh):
    """Cập nhật ngành"""
    data = request.get_json()
    update_data = {}
    if "ten_nganh" in data:
        update_data["ten_nganh"] = data["ten_nganh"]
    if "ma_khoa" in data:
        update_data["ma_khoa"] = data["ma_khoa"]

    nganh = NganhService.update(ma_nganh, update_data)
    if nganh:
        return jsonify({"success": True, "data": nganh})
    return jsonify({"error": "Not Found", "message": "Ngành không tồn tại"}), 404


@nganh_bp.route("/<ma_nganh>", methods=["DELETE"])
@admin_required
def delete(ma_nganh):
    """Xóa ngành"""
    if NganhService.delete(ma_nganh):
        return jsonify({"success": True, "message": "Xóa ngành thành công"})
    return jsonify({"error": "Not Found", "message": "Ngành không tồn tại"}), 404


@nganh_bp.route("/<ma_nganh>/lop", methods=["GET"])
def get_lop(ma_nganh):
    """Lấy danh sách lớp thuộc ngành"""
    result = NganhService.get_lop_by_nganh(ma_nganh)
    if result["success"]:
        return jsonify(result)
    return jsonify({"error": "Not Found", "message": result["message"]}), 404

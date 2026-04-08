"""
Khoa Routes - CRUD endpoints cho Khoa
"""
from flask import Blueprint, request, jsonify

from app.services.khoa_service import KhoaService
from app.middleware.jwt_auth import admin_required

khoa_bp = Blueprint("khoa", __name__)


@khoa_bp.route("/", methods=["GET"])
def index():
    """Lấy danh sách khoa"""
    khoas = KhoaService.get_all(order_by="ma_khoa")
    return jsonify({"success": True, "data": khoas})


@khoa_bp.route("/<ma_khoa>", methods=["GET"])
def show(ma_khoa):
    """Lấy thông tin khoa"""
    khoa = KhoaService.get_by_id(ma_khoa)
    if not khoa:
        return jsonify({"error": "Not Found", "message": "Khoa không tồn tại"}), 404
    return jsonify({"success": True, "data": khoa})


@khoa_bp.route("/", methods=["POST"])
@admin_required
def create():
    """Tạo khoa mới"""
    data = request.get_json()
    result = KhoaService.create_with_validation(
        data.get("ma_khoa"),
        data.get("ten_khoa"),
        data.get("mo_ta")
    )
    if result["success"]:
        return jsonify(result), 201
    return jsonify({"error": "Bad Request", "message": result["message"]}), 400


@khoa_bp.route("/<ma_khoa>", methods=["PUT"])
@admin_required
def update(ma_khoa):
    """Cập nhật khoa"""
    data = request.get_json()
    khoa = KhoaService.update(ma_khoa, {"ten_khoa": data.get("ten_khoa"), "mo_ta": data.get("mo_ta")})
    if khoa:
        return jsonify({"success": True, "data": khoa})
    return jsonify({"error": "Not Found", "message": "Khoa không tồn tại"}), 404


@khoa_bp.route("/<ma_khoa>", methods=["DELETE"])
@admin_required
def delete(ma_khoa):
    """Xóa khoa"""
    if KhoaService.delete(ma_khoa):
        return jsonify({"success": True, "message": "Xóa khoa thành công"})
    return jsonify({"error": "Not Found", "message": "Khoa không tồn tại"}), 404


@khoa_bp.route("/<ma_khoa>/nganh", methods=["GET"])
def get_nganh(ma_khoa):
    """Lấy danh sách ngành thuộc khoa"""
    result = KhoaService.get_nganh_by_khoa(ma_khoa)
    if result["success"]:
        return jsonify(result)
    return jsonify({"error": "Not Found", "message": result["message"]}), 404

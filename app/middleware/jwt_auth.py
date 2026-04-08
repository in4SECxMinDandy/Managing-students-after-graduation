"""
JWT Authentication Middleware
Tạo và verify JWT tokens cho 2 vai trò: admin, student
"""
import jwt
from datetime import datetime, timedelta, timezone
from functools import wraps
from flask import request, jsonify, g

from config import Config


def generate_token(payload: dict, role: str) -> str:
    """
    Tạo JWT token với role
    payload: dict chứa user data (MaAdmin/MaSV/MaTK, email, etc.)
    role: 'admin' | 'student'
    """
    token_payload = {
        **payload,
        "role": role,
        "exp": datetime.now(timezone.utc) + timedelta(hours=Config.JWT_EXPIRY_HOURS),
        "iat": datetime.now(timezone.utc)
    }
    return jwt.encode(token_payload, Config.JWT_SECRET, algorithm=Config.JWT_ALGORITHM)


def decode_token(token: str) -> dict:
    """Decode và verify JWT token"""
    try:
        return jwt.decode(token, Config.JWT_SECRET, algorithms=[Config.JWT_ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise ValueError("Token đã hết hạn")
    except jwt.InvalidTokenError:
        raise ValueError("Token không hợp lệ")


def get_token_from_header() -> str:
    """Lấy token từ Authorization header"""
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        raise ValueError("Không tìm thấy Authorization header")
    parts = auth_header.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise ValueError("Authorization header format không hợp lệ")
    return parts[1]


def jwt_required(f):
    """Decorator yêu cầu JWT token hợp lệ"""
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            token = get_token_from_header()
            payload = decode_token(token)
            g.current_user = payload
            g.role = payload.get("role")
            return f(*args, **kwargs)
        except ValueError as e:
            return jsonify({"error": "Unauthorized", "message": str(e)}), 401
    return decorated


def role_required(*allowed_roles):
    """Decorator kiểm tra role có quyền truy cập"""
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            try:
                token = get_token_from_header()
                payload = decode_token(token)
                g.current_user = payload
                g.role = payload.get("role")
                if g.role not in allowed_roles:
                    return jsonify({
                        "error": "Forbidden",
                        "message": f"Role '{g.role}' không có quyền truy cập endpoint này"
                    }), 403
                return f(*args, **kwargs)
            except ValueError as e:
                return jsonify({"error": "Unauthorized", "message": str(e)}), 401
        return decorated
    return decorator


# Convenience decorators
admin_required = role_required("admin")
student_required = role_required("student")
admin_or_student = role_required("admin", "student")

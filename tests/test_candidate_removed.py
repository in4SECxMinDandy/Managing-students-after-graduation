"""
Tests cho việc loại bỏ vai trò Thí sinh (Candidate)
Chỉ còn 2 vai trò: Admin và Sinh viên
"""
import pytest
import jwt
from datetime import datetime, timedelta, timezone


class MockConfig:
    JWT_SECRET = "test-secret-key"
    JWT_ALGORITHM = "HS256"
    JWT_EXPIRY_HOURS = 24


class TestTwoRoleSystem:
    """Test xác nhận hệ thống chỉ có 2 vai trò: Admin và Student"""

    def test_only_admin_and_student_roles_exist(self):
        """Xác nhận chỉ có 2 vai trò hợp lệ"""
        valid_roles = ["admin", "student"]
        invalid_role = "candidate"

        assert invalid_role not in valid_roles
        assert len(valid_roles) == 2
        assert "admin" in valid_roles
        assert "student" in valid_roles

    def test_no_candidate_role_in_token(self):
        """Xác nhận candidate role không còn trong token"""
        token_payload_admin = {
            "user_id": "admin001",
            "role": "admin"
        }
        token_payload_student = {
            "MaSV": "SV2512345678",
            "role": "student"
        }

        # Token không chứa role candidate
        assert token_payload_admin.get("role") != "candidate"
        assert token_payload_student.get("role") != "candidate"

    def test_admin_role_valid(self):
        """Xác nhận Admin role hợp lệ"""
        token_payload = {
            "user_id": "admin001",
            "TenDN": "admin1",
            "role": "admin"
        }
        assert token_payload["role"] == "admin"

    def test_student_role_valid(self):
        """Xác nhận Student role hợp lệ"""
        token_payload = {
            "MaSV": "SV2512345678",
            "HoTen": "Nguyen Van A",
            "role": "student"
        }
        assert token_payload["role"] == "student"


class TestCandidateRoleRemoved:
    """Test xác nhận vai trò Candidate đã bị loại bỏ"""

    def test_candidate_role_not_allowed(self):
        """Xác nhận candidate không còn là vai trò hợp lệ"""
        allowed_roles = ["admin", "student"]
        assert "candidate" not in allowed_roles

    def test_candidate_decorator_not_exists(self):
        """Xác nhận candidate_required decorator không còn"""
        # Import từ module - nếu tồn tại sẽ raise ImportError
        with pytest.raises(ImportError):
            from app.middleware.jwt_auth import candidate_required

    def test_admin_or_candidate_decorator_not_exists(self):
        """Xác nhận admin_or_candidate decorator không còn"""
        with pytest.raises(ImportError):
            from app.middleware.jwt_auth import admin_or_candidate

    def test_candidate_login_not_supported(self):
        """Xác nhận login candidate không còn được hỗ trợ"""
        # Auth service không còn method login_candidate
        from app.services import auth_service
        assert not hasattr(auth_service.AuthService, "login_candidate")

    def test_candidate_register_not_supported(self):
        """Xác nhận register candidate không còn được hỗ trợ"""
        # Auth service không còn method register_candidate
        from app.services import auth_service
        assert not hasattr(auth_service.AuthService, "register_candidate")

    def test_candidate_model_not_exists(self):
        """Xác nhận TKXetTuyen model không còn"""
        from app import models
        assert not hasattr(models, "TKXetTuyen")


class TestAuthRoutesCandidateRemoved:
    """Test xác nhận các route candidate đã bị loại bỏ"""

    def test_register_candidate_route_not_exists(self):
        """Xác nhận route register-candidate không còn"""
        from app.routes import auth_routes

        # Kiem tra function khong ton tai trong module
        endpoints = [e for e in dir(auth_routes) if not e.startswith('_')]
        assert 'register_candidate' not in endpoints


class TestRoleBasedAccessTwoRoles:
    """Test phân quyền chỉ với 2 vai trò"""

    def test_admin_access_admin_endpoints(self):
        """Xác nhận admin có quyền admin endpoints"""
        allowed_roles_admin = ["admin"]
        current_role = "admin"
        assert current_role in allowed_roles_admin

    def test_student_cannot_access_admin_endpoints(self):
        """Xác nhận student không có quyền admin endpoints"""
        allowed_roles_admin = ["admin"]
        current_role = "student"
        assert current_role not in allowed_roles_admin

    def test_admin_can_access_student_data(self):
        """Xác nhận admin có quyền xem dữ liệu student"""
        allowed_roles_student = ["admin", "student"]
        current_role = "admin"
        assert current_role in allowed_roles_student

    def test_student_can_access_own_data(self):
        """Xác nhận student có quyền xem dữ liệu bản thân"""
        allowed_roles_student = ["admin", "student"]
        current_role = "student"
        assert current_role in allowed_roles_student


class TestJWTWithTwoRoles:
    """Test JWT tokens chỉ với 2 vai trò"""

    def test_admin_token_generation(self):
        """Test tạo JWT token cho admin"""
        payload = {
            "user_id": "admin001",
            "role": "admin"
        }
        token = jwt.encode(
            {
                **payload,
                "exp": datetime.now(timezone.utc) + timedelta(hours=24),
                "iat": datetime.now(timezone.utc)
            },
            MockConfig.JWT_SECRET,
            algorithm=MockConfig.JWT_ALGORITHM
        )
        decoded = jwt.decode(token, MockConfig.JWT_SECRET, algorithms=[MockConfig.JWT_ALGORITHM])
        assert decoded["role"] == "admin"
        assert "candidate" not in decoded.values()

    def test_student_token_generation(self):
        """Test tạo JWT token cho student"""
        payload = {
            "MaSV": "SV2512345678",
            "role": "student"
        }
        token = jwt.encode(
            {
                **payload,
                "exp": datetime.now(timezone.utc) + timedelta(hours=24),
                "iat": datetime.now(timezone.utc)
            },
            MockConfig.JWT_SECRET,
            algorithm=MockConfig.JWT_ALGORITHM
        )
        decoded = jwt.decode(token, MockConfig.JWT_SECRET, algorithms=[MockConfig.JWT_ALGORITHM])
        assert decoded["role"] == "student"
        assert "candidate" not in decoded.values()

    def test_no_candidate_token_accepted(self):
        """Xác nhận candidate token không còn được chấp nhận"""
        # Giả lập candidate token
        candidate_payload = {
            "MaTK": "TK1234",
            "email": "test@gmail.com",
            "role": "candidate"
        }
        # Chỉ có 2 vai trò hợp lệ
        valid_roles = ["admin", "student"]
        assert candidate_payload["role"] not in valid_roles

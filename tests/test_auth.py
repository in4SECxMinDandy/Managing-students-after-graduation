"""
Tests cho Authentication
Chạy: pytest tests/test_auth.py -v
"""
import pytest
import jwt
from datetime import datetime, timedelta, timezone
from werkzeug.security import generate_password_hash, check_password_hash

# Mock config for testing
class MockConfig:
    JWT_SECRET = "test-secret-key"
    JWT_ALGORITHM = "HS256"
    JWT_EXPIRY_HOURS = 24


class TestJWTToken:
    """Test JWT token generation và verification"""

    def test_generate_token(self):
        """Test tạo JWT token"""
        payload = {"user_id": "123", "role": "admin"}
        token = jwt.encode(
            {
                **payload,
                "exp": datetime.now(timezone.utc) + timedelta(hours=24),
                "iat": datetime.now(timezone.utc)
            },
            MockConfig.JWT_SECRET,
            algorithm=MockConfig.JWT_ALGORITHM
        )
        assert token is not None
        assert isinstance(token, str)

    def test_decode_token(self):
        """Test decode JWT token"""
        payload = {"user_id": "123", "role": "admin"}
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
        assert decoded["user_id"] == "123"
        assert decoded["role"] == "admin"

    def test_expired_token(self):
        """Test token hết hạn"""
        payload = {"user_id": "123", "role": "admin"}
        token = jwt.encode(
            {
                **payload,
                "exp": datetime.now(timezone.utc) - timedelta(hours=1),
                "iat": datetime.now(timezone.utc) - timedelta(hours=2)
            },
            MockConfig.JWT_SECRET,
            algorithm=MockConfig.JWT_ALGORITHM
        )

        with pytest.raises(jwt.ExpiredSignatureError):
            jwt.decode(token, MockConfig.JWT_SECRET, algorithms=[MockConfig.JWT_ALGORITHM])

    def test_invalid_token(self):
        """Test token không hợp lệ"""
        with pytest.raises(jwt.InvalidTokenError):
            jwt.decode("invalid.token.here", MockConfig.JWT_SECRET, algorithms=[MockConfig.JWT_ALGORITHM])

    def test_wrong_secret(self):
        """Test token sign với secret khác"""
        token = jwt.encode(
            {"user_id": "123"},
            "secret-1",
            algorithm=MockConfig.JWT_ALGORITHM
        )

        with pytest.raises(jwt.InvalidSignatureError):
            jwt.decode(token, "secret-2", algorithms=[MockConfig.JWT_ALGORITHM])


class TestPasswordHashing:
    """Test password hashing với werkzeug"""

    def test_hash_password(self):
        """Test hash password"""
        password = "mysecretpassword123"
        hashed = generate_password_hash(password)

        assert hashed != password
        assert len(hashed) > 0
        assert hashed.startswith("scrypt:")

    def test_verify_password_correct(self):
        """Test verify password đúng"""
        password = "mysecretpassword123"
        hashed = generate_password_hash(password)

        assert check_password_hash(hashed, password) == True

    def test_verify_password_incorrect(self):
        """Test verify password sai"""
        password = "mysecretpassword123"
        hashed = generate_password_hash(password)

        assert check_password_hash(hashed, "wrongpassword") == False

    def test_different_passwords_different_hashes(self):
        """Test hai password khác nhau cho hash khác nhau"""
        hash1 = generate_password_hash("password1")
        hash2 = generate_password_hash("password2")

        assert hash1 != hash2


class TestRoleBasedAccess:
    """Test phân quyền theo vai trò"""

    def test_admin_role(self):
        """Test role admin"""
        token_payload = {
            "user_id": "admin001",
            "TenDN": "admin1",
            "role": "admin"
        }
        assert token_payload["role"] == "admin"

    def test_student_role(self):
        """Test role student"""
        token_payload = {
            "MaSV": "SV2512345678",
            "HoTen": "Nguyen Van A",
            "role": "student"
        }
        assert token_payload["role"] == "student"

    def test_candidate_role(self):
        """Test role candidate"""
        token_payload = {
            "MaTK": "TK1234",
            "Email": "test@gmail.com",
            "role": "candidate"
        }
        assert token_payload["role"] == "candidate"

    def test_role_comparison(self):
        """Test so sánh role"""
        allowed_roles_admin = ["admin"]
        allowed_roles_student = ["admin", "student"]
        allowed_roles_all = ["admin", "student", "candidate"]

        current_role = "student"

        assert current_role in allowed_roles_student
        assert current_role not in allowed_roles_admin
        assert current_role in allowed_roles_all


class TestLoginValidation:
    """Test validation cho login"""

    def test_empty_username(self):
        """Test username rỗng"""
        username = ""
        assert not username.strip()

    def test_empty_password(self):
        """Test password rỗng"""
        password = ""
        assert not password

    def test_email_validation_gmail(self):
        """Test email phải là @gmail.com"""
        valid_email = "test@gmail.com"
        invalid_email = "test@yahoo.com"

        assert valid_email.endswith("@gmail.com")
        assert not invalid_email.endswith("@gmail.com")

    def test_ma_sv_format_login(self):
        """Test format MaSV khi login"""
        valid_ma_sv = "SV2512345678"
        invalid_ma_sv = "SV25"  # Quá ngắn

        assert len(valid_ma_sv) == 10
        assert len(invalid_ma_sv) < 10

# AUTH - Kiến trúc Xác thực

## Tổng quan

Hệ thống xác thực QLSVSDH sử dụng **JWT (JSON Web Token)** với **3 vai trò** riêng biệt.

## 3 Vai trò người dùng

### 1. Admin (Quản trị viên)

- **Nguồn dữ liệu**: Bảng `QuanTri`
- **Đăng nhập**: Tên đăng nhập (TenDN) + Mật khẩu
- **Quyền hạn**:
  - CRUD tất cả module (Khoa, Ngành, Lớp, Môn học, Sinh viên)
  - Duyệt/từ chối tuyển sinh
  - Gửi thông báo

### 2. Sinh viên (Student)

- **Nguồn dữ liệu**: Bảng `SinhVien`
- **Đăng nhập**: Mã sinh viên (MaSV) + Mật khẩu
- **Quyền hạn**:
  - Xem điểm, GPA của bản thân
  - Xem trạng thái tốt nghiệp
  - Đọc thông báo

### 3. Thí sinh (Candidate)

- **Nguồn dữ liệu**: Bảng `TK_XETTUYEN`
- **Đăng nhập**: Email + Mật khẩu
- **Quyền hạn**:
  - Đăng ký tài khoản mới
  - Nộp hồ sơ xét tuyển
  - Xem trạng thái đơn đăng ký

## JWT Token Structure

```json
{
  "MaAdmin|MaSV|MaTK": "...",
  "email|TenDN|HoTen": "...",
  "role": "admin|student|candidate",
  "exp": "...",
  "iat": "..."
}
```

## Auth Flow

```
┌─────────────────────────────────────────────────────────────┐
│                    AUTHENTICATION FLOW                       │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  User ──► Login ──► Validate ──► Generate JWT ──► Response │
│                      │                                       │
│                      ▼                                       │
│               Check password                                 │
│               (werkzeug)                                    │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐    │
│  │ JWT Token Format: Bearer <token>                     │    │
│  │ Header: Authorization: Bearer eyJhbGci...            │    │
│  └──────────────────────────────────────────────────────┘    │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## API Endpoints

### POST /api/auth/login

```python
# Admin login
{
    "role": "admin",
    "ten_dn": "admin1",
    "mat_khau": "password123"
}

# Student login
{
    "role": "student",
    "ma_sv": "SV20250001",
    "mat_khau": "password123"
}

# Candidate login
{
    "role": "candidate",
    "email": "test@gmail.com",
    "mat_khau": "password123"
}

# Response
{
    "success": True,
    "token": "eyJhbGciOiJIUzI1NiIs...",
    "user": {
        "MaAdmin|MaSV|MaTK": "...",
        "role": "admin|student|candidate"
    }
}
```

### POST /api/auth/register-candidate

```python
{
    "email": "candidate@gmail.com",
    "mat_khau": "password123"
}
```

## Middleware Protection

### Decorators

| Decorator | Mô tả |
|-----------|--------|
| `@jwt_required` | Yêu cầu đăng nhập (bất kỳ role) |
| `@admin_required` | Chỉ Admin |
| `@student_required` | Chỉ Sinh viên |
| `@candidate_required` | Chỉ Thí sinh |
| `@admin_or_student` | Admin hoặc Sinh viên |
| `@admin_or_candidate` | Admin hoặc Thí sinh |

### Sử dụng

```python
from app.middleware.jwt_auth import admin_required, student_required

@admin_required
def admin_only_endpoint():
    ma_admin = g.current_user["MaAdmin"]
    # ...

@student_required
def student_only_endpoint():
    ma_sv = g.current_user["MaSV"]
    # ...
```

## Password Hashing

Sử dụng `werkzeug.security`:

```python
from werkzeug.security import generate_password_hash, check_password_hash

# Hash password
hashed = generate_password_hash("password123")

# Verify password
check_password_hash(hashed, "password123")  # True/False
```

## Business Rules

### Admin

- Mật khẩu phải được hash trước khi lưu
- TenDN phải unique

### Candidate

- Email phải có đuôi `@gmail.com`
- Email phải unique
- Mật khẩu tối thiểu 6 ký tự

### Student

- Mật khẩu tối thiểu 6 ký tự
- Email phải unique

## Demo Credentials

Sau khi import `database.sql` với seeders:

| Role | Username | Password |
|------|----------|----------|
| Admin | admin1 | admin123 |
| Student | SV20250001 | 123456 |
| Candidate | test@gmail.com | 123456 |

## Security Notes

1. **JWT Secret**: Thay đổi trong `config.py` cho production
2. **Password**: Luôn hash, không bao giờ lưu plain text
3. **Token Expiry**: Mặc định 24 giờ
4. **CORS**: Đang mở cho tất cả origins (chỉnh sửa cho production)

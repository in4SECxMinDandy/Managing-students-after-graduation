# Auth Module

## Mô tả

Module xác thực và phân quyền người dùng. Bao gồm quản lý **QuanTri**, **SinhVien**, **GiangVien** và JWT authentication.

## API Endpoints

### Authentication
- `POST /auth/login` — Đăng nhập (username/email + password → JWT tokens)
- `POST /auth/refresh` — Refresh access token

### Admin Users
- `GET /auth/admins` — Danh sách admin
- `POST /auth/admins` — Tạo admin mới
- `GET /auth/admins/{ma_admin}` — Chi tiết admin
- `PUT /auth/admins/{ma_admin}` — Cập nhật admin
- `DELETE /auth/admins/{ma_admin}` — Xóa mềm admin

### Students
- `GET /auth/students` — Danh sách sinh viên
- `POST /auth/students` — Tạo sinh viên mới
- `GET /auth/students/{ma_sv}` — Chi tiết sinh viên
- `PUT /auth/students/{ma_sv}` — Cập nhật sinh viên
- `DELETE /auth/students/{ma_sv}` — Xóa mềm sinh viên

### Lecturers
- `GET /auth/lecturers` — Danh sách giảng viên
- `POST /auth/lecturers` — Tạo giảng viên mới
- `GET /auth/lecturers/{ma_gv}` — Chi tiết giảng viên
- `PUT /auth/lecturers/{ma_gv}` — Cập nhật giảng viên
- `DELETE /auth/lecturers/{ma_gv}` — Xóa mềm giảng viên

## Phân quyền

| Endpoint | Role được phép |
|----------|----------------|
| Tạo/Sửa/Xóa Admin | `admin`, `super_admin` |
| Tạo/Sửa/Xóa SinhVien | `admin`, `super_admin` |
| Tạo/Sửa/Xóa GiangVien | `admin`, `super_admin` |
| Xem danh sách | Tất cả role |

## Business Rules

- Mật khẩu được bcrypt-hash trước khi lưu
- JWT access token hết hạn sau `ACCESS_TOKEN_EXPIRE_MINUTES` (mặc định 1440 phút)
- Refresh token hết hạn sau `REFRESH_TOKEN_EXPIRE_DAYS` (mặc định 7 ngày)

# QLSVSDH - Hệ thống Quản lý Sinh viên Đại học

> **100% Python + XAMPP** - Flask API Backend + Tkinter GUI + MySQL

## Mục lục

1. [Tổng quan](#tổng-quan)
2. [Kiến trúc](#kiến-trúc)
3. [Cài đặt](#cài-đặt)
4. [Chạy ứng dụng](#chạy-ứng-dụng)
5. [Modules](#modules)
6. [Business Rules](#business-rules)
7. [API Endpoints](#api-endpoints)
8. [Cấu trúc thư mục](#cấu-trúc-thư-mục)

---

## Tổng quan

QLSVSDH là hệ thống quản lý sinh viên đại học hoàn chỉnh, được xây dựng bằng:

- **Backend**: Python Flask API
- **Frontend**: Python Tkinter GUI (chạy `python gui.py`)
- **Database**: MySQL (XAMPP)
- **Authentication**: JWT với 2 vai trò

### 2 Vai trò người dùng

| Vai trò | Mô tả | Quyền hạn |
|---------|--------|-----------|
| **Admin** | Quản trị viên | Quản lý Khoa, Ngành, Lớp, Môn học, Sinh viên, Thông báo |
| **Sinh viên** | Sinh viên | Xem điểm, GPA, xếp loại tốt nghiệp, thông báo |

---

## Kiến trúc

```
┌──────────────────────────────────────────────┐
│          Python GUI (gui.py / Tkinter)       │
│  - Cửa sổ đăng nhập theo vai trò            │
│  - Dashboard theo role (Admin/SV)   │
│  - CRUD cho từng module                      │
└───────────────┬──────────────────────────────┘
                │ REST API (requests lib)
┌───────────────▼──────────────────────────────┐
│           Flask API (app/)                   │
│  ├── routes/     (Blueprints theo module)    │
│  ├── services/   (Business logic)            │
│  ├── models/     (MySQL Connector)           │
│  ├── schemas/    (Validators)                 │
│  └── middleware/ (JWT Auth, Role Guard)       │
└───────────────┬──────────────────────────────┘
                │ mysql-connector-python
┌───────────────▼──────────────────────────────┐
│           XAMPP MySQL (database)              │
└──────────────────────────────────────────────┘
```

### 3-Tier Architecture

| Lớp | Mô tả | Files |
|-----|-------|-------|
| **Presentation** | Tkinter GUI | `gui.py` |
| **Business** | Flask Routes + Services | `app/routes/`, `app/services/` |
| **Data** | MySQL Models | `app/models/` |

---

## Cài đặt

### 1. Yêu cầu

- Python 3.10+
- XAMPP (MySQL)
- Git

### 2. Clone và cài đặt dependencies

```bash
cd QLSVSDH
pip install -r requirements.txt
```

### 3. Cài đặt XAMPP

1. Tải và cài đặt [XAMPP](https://www.apachefriends.org/)
2. Bật **Apache** và **MySQL** trong XAMPP Control Panel
3. Tạo database `qlsvsdh`:

```sql
-- Truy cập phpMyAdmin: http://localhost/phpmyadmin
CREATE DATABASE qlsvsdh CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

4. Import schema từ `database.sql`

### 4. Cấu hình

Chỉnh sửa `config.py` nếu cần:

```python
MYSQL_HOST = "localhost"
MYSQL_PORT = 3306
MYSQL_USER = "root"
MYSQL_PASSWORD = ""        # XAMPP default
MYSQL_DATABASE = "qlsvsdh"
JWT_SECRET = "your-secret-key"
```

---

## Chạy ứng dụng

### Terminal 1: Khởi động Flask API

```bash
python run.py
```

Output:
```
==================================================
QLSVSDH API Server
==================================================
Starting Flask server...
API Endpoints: http://localhost:5000/api/
Health Check:  http://localhost:5000/api/health
==================================================
```

### Terminal 2: Chạy GUI

```bash
python gui.py
```

---

## Modules

Mỗi module có cấu trúc:

```
app/
├── models/
│   ├── base.py              # BaseModel - CRUD foundation
│   └── {module}.py         # Model class
├── services/
│   ├── base_service.py     # BaseService - business logic foundation
│   └── {module}_service.py # Service class
└── routes/
    └── {module}_routes.py  # API endpoints
```

### Các module đã implement

| Module | Mô tả | Bảng DB |
|--------|-------|---------|
| **Khoa** | Quản lý Khoa | Khoa |
| **MonHoc** | Quản lý Môn học | MonHoc |
| **Nganh** | Quản lý Ngành | Nganh |
| **Lop** | Quản lý Lớp | Lop |
| **SinhVien** | Quản lý Sinh viên | SinhVien |
| **HocTap** | Quản lý Kết quả học tập | KQ_HocTap |
| **TotNghiep** | Xét tốt nghiệp | TotNghiep |
| **ThongBao** | Quản lý Thông báo | ThongBao, TB_NguoiNhan |

Xem chi tiết từng module trong thư mục `docs/`:
- [Khoa.md](docs/Khoa.md)
- [MonHoc.md](docs/MonHoc.md)
- [Nganh.md](docs/Nganh.md)
- [Lop.md](docs/Lop.md)
- [SinhVien.md](docs/SinhVien.md)
- [HocTap.md](docs/HocTap.md)
- [TotNghiep.md](docs/TotNghiep.md)
- [ThongBao.md](docs/ThongBao.md)
- [AUTH.md](docs/AUTH.md) - Chi tiết xác thực

---

## Business Rules

### Validation Rules

| Bảng | Trường | Quy tắc |
|------|--------|---------|
| KQ_HocTap | Diem | 0-10 |
| SinhVien | NgaySinh | Không future |

### GPA Calculation

```
GPA (thang 4) = GPA (thang 10) / 2.5
GPA (thang 10) = Σ(Diem × SoTinChi) / Σ(SoTinChi)
```

### Xếp loại tốt nghiệp

| GPA (thang 4) | Xếp loại |
|---------------|----------|
| ≥ 3.60 | Xuất sắc |
| ≥ 3.20 | Giỏi |
| ≥ 2.50 | Khá |
| ≥ 2.00 | Trung bình |
| < 2.00 | Yếu |

---

## API Endpoints

### Authentication

| Method | Endpoint | Mô tả | Auth |
|--------|----------|--------|------|
| POST | `/api/auth/login` | Đăng nhập | No |
| POST | `/api/auth/change-password` | Đổi mật khẩu | JWT |
| GET | `/api/auth/me` | Thông tin user | JWT |

### Khoa

| Method | Endpoint | Mô tả | Auth |
|--------|----------|--------|------|
| GET | `/api/khoa/` | Danh sách khoa | No |
| GET | `/api/khoa/<ma_khoa>` | Chi tiết khoa | No |
| POST | `/api/khoa/` | Tạo khoa | Admin |
| PUT | `/api/khoa/<ma_khoa>` | Cập nhật | Admin |
| DELETE | `/api/khoa/<ma_khoa>` | Xóa khoa | Admin |
| GET | `/api/khoa/<ma_khoa>/nganh` | Ngành thuộc khoa | No |

### Học tập

| Method | Endpoint | Mô tả | Auth |
|--------|----------|--------|------|
| GET | `/api/hoc-tap/diem/<ma_sv>` | Bảng điểm | Admin/SV |
| POST | `/api/hoc-tap/diem` | Nhập điểm | Admin |
| GET | `/api/hoc-tap/gpa/<ma_sv>` | Tính GPA | Admin/SV |

### Tốt nghiệp

| Method | Endpoint | Mô tả | Auth |
|--------|----------|--------|------|
| GET | `/api/tot-nghiep/check/<ma_sv>` | Xét tốt nghiệp | Admin/SV |
| GET | `/api/tot-nghiep/status/<ma_sv>` | Trạng thái | Admin/SV |
| GET | `/api/tot-nghiep/all` | Danh sách tốt nghiệp | Admin |

---

## Cấu trúc thư mục

```
QLSVSDH/
├── README.md              # File này
├── database.sql           # Schema MySQL
├── requirements.txt       # Python dependencies
├── config.py              # Cấu hình
├── run.py                 # Flask API entry point
├── gui.py                 # Tkinter GUI entry point
│
├── app/                   # Flask API
│   ├── __init__.py       # App factory
│   ├── models/           # Database models
│   │   ├── base.py
│   │   ├── khoa.py
│   │   ├── mon_hoc.py
│   │   ├── quan_tri.py
│   │   ├── nganh.py
│   │   ├── lop.py
│   │   ├── sinh_vien.py
│   │   ├── thong_bao.py
│   │   ├── kq_hoc_tap.py
│   │   └── tot_nghiep.py
│   ├── services/         # Business logic
│   │   ├── base_service.py
│   │   ├── auth_service.py
│   │   ├── khoa_service.py
│   │   ├── mon_hoc_service.py
│   │   ├── nganh_service.py
│   │   ├── lop_service.py
│   │   ├── sinh_vien_service.py
│   │   ├── hoc_tap_service.py
│   │   ├── tot_nghiep_service.py
│   │   └── thong_bao_service.py
│   ├── routes/           # API endpoints
│   │   ├── auth_routes.py
│   │   ├── khoa_routes.py
│   │   ├── mon_hoc_routes.py
│   │   ├── nganh_routes.py
│   │   ├── lop_routes.py
│   │   ├── sinh_vien_routes.py
│   │   ├── tuyen_sinh_routes.py
│   │   ├── hoc_tap_routes.py
│   │   ├── tot_nghiep_routes.py
│   │   └── thong_bao_routes.py
│   └── middleware/       # JWT Auth
│       └── jwt_auth.py
│
├── docs/                  # Module documentation
│   ├── README.md
│   ├── AUTH.md
│   ├── Khoa.md
│   ├── MonHoc.md
│   ├── Nganh.md
│   ├── Lop.md
│   ├── TuyenSinh.md
│   ├── SinhVien.md
│   ├── HocTap.md
│   ├── TotNghiep.md
│   └── ThongBao.md
│
└── tests/                 # Unit tests
    ├── __init__.py
    ├── test_auth.py
    ├── test_gpa.py
    └── test_business_rules.py
```

---

## License

MIT License

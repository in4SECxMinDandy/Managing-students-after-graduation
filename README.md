# Hệ thống Quản lý Sinh viên Sau Đại học (QLSVSDH)

> Nền tảng quản lý toàn diện cho sinh viên sau đại học — từ tuyển sinh, đào tạo, luận văn, tài chính đến hỗ trợ sinh viên.

---

## Mục lục

- [Tổng quan](#tổng-quan)
- [Công nghệ sử dụng](#công-nghệ-sử-dụng)
- [Kiến trúc hệ thống](#kiến-trúc-hệ-thống)
- [Yêu cầu hệ thống](#yêu-cầu-hệ-thống)
- [Cài đặt & Khởi chạy](#cài-đặt--khởi-chạy)
- [Cấu hình môi trường](#cấu-hình-môi-trường)
- [Tài khoản mặc định](#tài-khoản-mặc-định)
- [API Endpoints](#api-endpoints)
- [Database Schema](#database-schema)
- [Business Rules](#business-rules)
- [Phân quyền (RBAC)](#phân-quyền-rbac)
- [Modules chi tiết](#modules-chi-tiết)
- [Kiểm thử](#kiểm-thử)

---

## Tổng quan

**QLSVSDH** là hệ thống quản lý sinh viên sau đại học được xây dựng hoàn toàn bằng **Python**, theo kiến trúc **Clean Architecture** gồm 3 tầng:

| Tầng | Công nghệ | Mô tả |
| --- | --- | --- |
| **Backend API** | FastAPI + SQLAlchemy | REST API bất đồng bộ, JWT auth |
| **Frontend Web** | Streamlit | Giao diện web đơn giản cho admin |
| **Frontend GUI** | PySide6 (Qt) | Ứng dụng desktop đa nền tảng |
| **Database** | PostgreSQL | Cơ sở dữ liệu quan hệ với 33 bảng |

---

## Công nghệ sử dụng

### Backend

| Thư viện | Phiên bản | Vai trò |
| --- | --- | --- |
| `fastapi` | ≥ 0.115 | Web framework |
| `uvicorn[standard]` | ≥ 0.32 | ASGI server |
| `sqlalchemy` | ≥ 2.0 | ORM (async) |
| `asyncpg` | ≥ 0.30 | PostgreSQL async driver |
| `alembic` | ≥ 1.14 | Database migrations |
| `pydantic` | ≥ 2.10 | Data validation |
| `python-jose` | ≥ 3.3 | JWT tokens |
| `passlib[bcrypt]` | ≥ 1.7 | Password hashing |

### Frontend GUI

| Thư viện | Phiên bản | Vai trò |
| --- | --- | --- |
| `PySide6` | ≥ 6.6 | Qt GUI framework |
| `qtpy` | ≥ 2.4 | Qt abstraction layer |
| `requests` | ≥ 2.31 | HTTP client gọi API |

### Dev Tools

| Công cụ | Vai trò |
| --- | --- |
| `pytest` + `pytest-asyncio` | Unit & integration tests |
| `ruff` | Linter & formatter |
| `mypy` | Static type checking |
| `httpx` | Async HTTP client for tests |

---

## Kiến trúc hệ thống

```text
QLSVSDH/
├── apps/                        # Business modules (Clean Architecture)
│   ├── auth/                    # Module 1: Xác thực & Phân quyền
│   │   ├── router.py            # FastAPI routes
│   │   ├── service.py           # Business logic
│   │   └── schemas.py           # Pydantic schemas
│   ├── admissions/              # Module 2: Tuyển sinh
│   │   ├── router.py
│   │   └── schemas.py
│   ├── training/                # Module 3: Đào tạo
│   │   ├── router.py
│   │   └── schemas.py
│   ├── thesis/                  # Module 4: Luận văn
│   │   ├── router.py
│   │   └── schemas.py
│   ├── finance/                 # Module 5: Tài chính
│   │   ├── router.py
│   │   └── schemas.py
│   └── support/                 # Module 6: Hỗ trợ
│       ├── router.py
│       └── schemas.py
├── backend/                     # Infrastructure layer
│   ├── config/settings.py       # Environment config (pydantic-settings)
│   ├── core/
│   │   ├── enums.py             # PostgreSQL enum mirrors
│   │   ├── exceptions.py        # Custom exception classes
│   │   ├── handlers.py          # FastAPI exception handlers
│   │   └── paginate.py          # Pagination utilities
│   ├── database/
│   │   ├── engine.py            # SQLAlchemy async engine & session
│   │   └── base_model.py        # Base model mixins (timestamps, soft delete)
│   ├── middleware/
│   │   ├── security.py          # JWT auth dependencies & role guards
│   │   └── cors.py              # CORS setup
│   ├── models/                  # SQLAlchemy ORM models (33 bảng)
│   ├── repositories/base.py     # Generic async repository
│   ├── schemas/                 # Shared Pydantic schemas
│   ├── services/                # Shared service base classes
│   └── utils/
│       ├── hash.py              # JWT & password utilities
│       ├── grade.py             # Grade scale conversion (10→4→letter)
│       ├── jwt.py               # Token encoding/decoding
│       └── pagination.py        # Paginated response helpers
├── frontend/
│   └── main.py                  # Streamlit web application
├── frontend_gui/                # PySide6 desktop application
│   ├── api/client.py            # HTTP client wrapper
│   ├── ui/                      # UI pages & widgets
│   └── main.py                  # Qt application entry point
├── alembic/                     # Database migrations
│   ├── env.py
│   └── versions/001_initial.py  # Initial migration (all 33 tables)
├── scripts/
│   └── seed.py                  # Seed dữ liệu mẫu (admin mặc định)
├── tests/                       # pytest test suite
├── schema_postgresql.sql        # Raw SQL schema (reference)
├── pyproject.toml               # Project config & dependencies
├── alembic.ini                  # Alembic config
└── .env.example                 # Mẫu biến môi trường
```

---

## Yêu cầu hệ thống

- **Python** ≥ 3.10
- **PostgreSQL** ≥ 14
- **pip** hoặc **uv** (package manager)

> **Lưu ý (Windows):** Nếu dùng Frontend GUI (PySide6), cần cài thêm `qtpy`:
>
> ```bash
> pip install qtpy PySide6
> ```

---

## Cài đặt & Khởi chạy

### 1. Clone repository

```bash
git clone https://github.com/in4SECxMinDandy/Managing-students-after-graduation.git
cd Managing-students-after-graduation
```

### 2. Cấu hình môi trường

```bash
cp .env.example .env
# Chỉnh sửa .env với thông tin database và secret key của bạn
```

### 3. Cài đặt dependencies

```bash
# Cài backend (bao gồm dev tools)
pip install -e ".[dev]"

# Cài frontend GUI (nếu cần)
pip install -r frontend_gui/requirements.txt
pip install qtpy
```

### 4. Khởi tạo database

```bash
# Chạy migrations để tạo toàn bộ 33 bảng
alembic upgrade head

# Seed dữ liệu mẫu (tạo tài khoản admin mặc định)
python scripts/seed.py
```

### 5. Khởi chạy Backend API

```bash
uvicorn backend.main:app --reload --port 8000
```

API sẽ hoạt động tại: `http://localhost:8000`
Tài liệu API tự động (Swagger): `http://localhost:8000/docs`
ReDoc: `http://localhost:8000/redoc`

### 6. Khởi chạy Frontend Web (Streamlit)

```bash
streamlit run frontend/main.py --server.port 8501
```

Truy cập tại: `http://localhost:8501`

### 7. Khởi chạy Frontend Desktop (PySide6)

```bash
python -m frontend_gui.main
```

---

## Cấu hình môi trường

Tạo file `.env` từ `.env.example` với các biến sau:

| Biến | Ví dụ | Mô tả |
| --- | --- | --- |
| `DATABASE_URL` | `postgresql+asyncpg://postgres:postgres@localhost:5432/qlsvsdh` | URL kết nối PostgreSQL |
| `SECRET_KEY` | `change-me-to-a-random-64-char-hex` | Khóa bí mật cho JWT |
| `ALGORITHM` | `HS256` | Thuật toán ký JWT |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `1440` | Thời gian sống access token (phút) |
| `REFRESH_TOKEN_EXPIRE_DAYS` | `7` | Thời gian sống refresh token (ngày) |
| `CORS_ORIGINS` | `http://localhost:8501,http://localhost:3000` | Danh sách origins được phép (phân cách bằng dấu phẩy) |

---

## Tài khoản mặc định

Sau khi chạy `python scripts/seed.py`:

| Trường | Giá trị |
| --- | --- |
| **Username** | `admin` |
| **Password** | `admin123` |
| **Role** | `admin` |
| **Email** | `admin@qlsvsdh.edu.vn` |

> ⚠️ **Quan trọng:** Đổi mật khẩu ngay sau khi đăng nhập lần đầu trong môi trường production.

---

## API Endpoints

### Authentication (`/auth`)

| Method | Endpoint | Mô tả | Phân quyền |
| --- | --- | --- | --- |
| `POST` | `/auth/login` | Đăng nhập, trả JWT token | Public |
| `POST` | `/auth/refresh` | Làm mới access token | Public |
| `POST` | `/auth/admins` | Tạo admin mới | Admin |
| `GET` | `/auth/admins` | Danh sách admins | Admin |
| `GET` | `/auth/admins/{id}` | Lấy thông tin admin | Admin |
| `PUT` | `/auth/admins/{id}` | Cập nhật admin | Admin |
| `DELETE` | `/auth/admins/{id}` | Xóa admin | Admin |
| `POST` | `/auth/students` | Tạo sinh viên mới | Admin |
| `GET` | `/auth/students` | Danh sách sinh viên | Đã xác thực |
| `GET` | `/auth/students/{id}` | Lấy thông tin sinh viên | Đã xác thực |
| `PUT` | `/auth/students/{id}` | Cập nhật sinh viên | Đã xác thực |
| `DELETE` | `/auth/students/{id}` | Xóa sinh viên | Admin |
| `POST` | `/auth/lecturers` | Tạo giảng viên mới | Admin |
| `GET` | `/auth/lecturers` | Danh sách giảng viên | Đã xác thực |
| `GET` | `/auth/lecturers/{id}` | Lấy thông tin giảng viên | Đã xác thực |
| `PUT` | `/auth/lecturers/{id}` | Cập nhật giảng viên | Đã xác thực |
| `DELETE` | `/auth/lecturers/{id}` | Xóa giảng viên | Admin |

> Xem toàn bộ API tại `http://localhost:8000/docs` sau khi khởi chạy server.

---

## Database Schema

Hệ thống sử dụng **33 bảng** PostgreSQL:

### Danh mục & Quản trị

| # | Bảng | Mô tả |
| --- | --- | --- |
| 1 | `Khoa` | Khoa/Viện trong trường |
| 2 | `Nganh` | Ngành đào tạo |
| 3 | `Lop` | Lớp học |
| 4 | `MonHoc` | Môn học |
| 5 | `HocKy` | Học kỳ |
| 6 | `QuanTri` | Tài khoản quản trị viên |
| 26 | `QuyDinhDacThu` | Quy định đặc thù theo khoa/ngành |
| 33 | `AuditLog` | Nhật ký kiểm toán tự động |

### Tuyển sinh

| # | Bảng | Mô tả |
| --- | --- | --- |
| 7 | `TK_XetTuyen` | Tài khoản xét tuyển |
| 8 | `HSO_XetTuyen` | Hồ sơ ứng tuyển |
| 9 | `PT_XetTuyen` | Phương thức xét tuyển |

### Đào tạo

| # | Bảng | Mô tả |
| --- | --- | --- |
| 10 | `SinhVien` | Sinh viên sau đại học |
| 11 | `GiangVien` | Giảng viên |
| 12 | `LopHocPhan` | Lớp học phần |
| 13 | `DangKyHocPhan` | Đăng ký học phần |
| 14 | `PhanCongGiangDay` | Phân công giảng dạy |
| 15 | `LichHoc` | Lịch học |
| 16 | `KQ_HocTap` | Kết quả học tập |
| 30 | `MonHocTienQuyet` | Môn học tiên quyết |
| 31 | `ChuongTrinhDaoTao` | Chương trình đào tạo |
| 32 | `LichThi` | Lịch thi |

### Luận văn

| # | Bảng | Mô tả |
| --- | --- | --- |
| 17 | `LuanVan` | Luận văn/Luận án |
| 18 | `DeCuongLuanAn` | Đề cương nghiên cứu |
| 24 | `NghienCuuKhoaHoc` | Công trình nghiên cứu khoa học |
| 25 | `TacGiaCongTrinh` | Tác giả công trình |
| 27 | `HoiDongBaoVe` | Hội đồng bảo vệ luận văn |
| 28 | `ThanhVienHoiDong` | Thành viên hội đồng |
| 29 | `ThuLaoHoiDong` | Thù lao hội đồng |

### Tài chính

| # | Bảng | Mô tả |
| --- | --- | --- |
| 19 | `DonGiaTinChi` | Đơn giá theo tín chỉ |
| 20 | `HocPhi` | Học phí sinh viên |
| 21 | `TotNghiep` | Xét tốt nghiệp |

### Hỗ trợ

| # | Bảng | Mô tả |
| --- | --- | --- |
| 22 | `ThongBao` | Thông báo hệ thống |
| 23 | `TB_NguoiNhan` | Người nhận thông báo |

---

## Business Rules

| Mã | Tên quy tắc | Mô tả chi tiết |
| --- | --- | --- |
| BR-01 | **Môn tiên quyết** | Sinh viên phải hoàn thành môn tiên quyết trước khi đăng ký môn phụ thuộc |
| BR-02 | **Giới hạn sĩ số** | `SiSoHienTai ≤ SiSoToiDa` — chỉ duyệt khi lớp còn chỗ |
| BR-03 | **Xung đột lịch** | Không trùng phòng/giảng viên cùng thứ, buổi, tiết trong một học kỳ |
| BR-04 | **Quy đổi điểm** | Tự động quy đổi thang 10 → thang 4 → điểm chữ khi nhập điểm |
| BR-05 | **Học phí tự động** | `SoTien = SoTinChi × DonGia` — trigger tự động khi duyệt đăng ký |
| BR-06 | **Phân công GV** | Mỗi giảng viên chỉ được 1 vai trò/lớp học phần; phải có Giảng viên chính |
| BR-07 | **Hội đồng BV** | Cần đủ 5 thành viên: `ChuTich`, `PhoChuTich`, `ThuKy`, `PhanBien1`, `PhanBien2` |
| BR-08 | **Xét tốt nghiệp** | GPA ≥ 3.6 → Xuất sắc · ≥ 3.2 → Giỏi · ≥ 2.5 → Khá · ≥ 2.0 → TB · < 2.0 → Yếu |
| BR-09 | **Ngày bảo vệ** | `NgayBaoVe ≥ NgayDangKy` — không được bảo vệ trước ngày đăng ký |
| BR-10 | **Audit Log** | Tự động ghi nhật ký INSERT/UPDATE/DELETE trên các bảng: `SinhVien`, `QuanTri`, `LuanVan`, `HocPhi`, `DangKyHocPhan` |

---

## Phân quyền (RBAC)

| Role | Mô tả | Quyền hạn |
| --- | --- | --- |
| `super_admin` | Quản trị viên cấp cao nhất | Toàn quyền, bao gồm tạo/xóa admin |
| `admin` | Quản trị viên | Quản lý sinh viên, giảng viên, dữ liệu hệ thống |
| `khoa` | Cán bộ khoa/viện | Quản lý dữ liệu trong phạm vi khoa |
| `giangvien` | Giảng viên | Xem lịch dạy, nhập điểm, quản lý luận văn |
| `sinhvien` | Sinh viên | Xem thông tin cá nhân, đăng ký học phần, xem điểm |

---

## Modules chi tiết

Mỗi module được tổ chức theo **Clean Architecture** với 3 lớp: Router → Service → Repository.

| Module | Tài liệu | Chức năng chính |
| --- | --- | --- |
| **Auth** | [apps/auth/README.md](apps/auth/README.md) | Đăng nhập JWT, quản lý admin/sinh viên/giảng viên |
| **Admissions** | [apps/admissions/README.md](apps/admissions/README.md) | Tuyển sinh, hồ sơ ứng tuyển, phương thức xét tuyển |
| **Training** | [apps/training/README.md](apps/training/README.md) | Học phần, lịch học, đăng ký, kết quả học tập |
| **Thesis** | [apps/thesis/README.md](apps/thesis/README.md) | Luận văn, đề cương, hội đồng bảo vệ, NCKH |
| **Finance** | [apps/finance/README.md](apps/finance/README.md) | Học phí, đơn giá tín chỉ, xét tốt nghiệp |
| **Support** | [apps/support/README.md](apps/support/README.md) | Thông báo, hỗ trợ sinh viên |

---

## Kiểm thử

```bash
# Chạy toàn bộ test suite
pytest

# Chạy với báo cáo coverage
pytest --cov=. --cov-report=html

# Chạy chỉ một module
pytest tests/test_grade.py -v

# Lint & format
ruff check .
ruff format .

# Type checking
mypy .
```

---

## Giấy phép

Dự án được cấp phép theo giấy phép **MIT**. Xem file [LICENSE](LICENSE) để biết thêm chi tiết.
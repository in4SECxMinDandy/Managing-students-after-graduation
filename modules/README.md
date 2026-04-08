# QLSVSDH — Hệ thống Quản lý Sinh viên Đại học

## Tổng quan

Hệ thống **QLSVSDH** được xây dựng trên **Laravel 11 + Livewire 3**, quản lý toàn bộ quy trình từ **xét tuyển → sinh viên → học tập → tốt nghiệp**.

## Kiến trúc 3 tầng

```
┌──────────────────────────────────────────────────────────────┐
│           Tầng Presentation (Livewire Components)             │
│  Livewire Components + Blade Templates + TailwindCSS          │
├──────────────────────────────────────────────────────────────┤
│              Tầng Service (Business Logic)                   │
│  AuthService, TuyenSinhService, HocTapService, etc.         │
├──────────────────────────────────────────────────────────────┤
│                Tầng Data (Eloquent ORM)                      │
│  Models + Repositories + Migrations + Seeders                  │
└──────────────────────────────────────────────────────────────┘
```

## 12 Module nghiệp vụ

| # | Module | Entities | Mô tả |
|---|--------|---------|--------|
| 1 | Auth | TK_XETTUYEN, QuanTri, SinhVien | Xác thực 3 role: candidate / student / admin |
| 2 | Khoa | Khoa | Quản lý Khoa |
| 3 | Nganh | Nganh | Quản lý Ngành (FK → Khoa) |
| 4 | Lop | Lop | Quản lý Lớp (FK → Nganh) |
| 5 | MonHoc | MonHoc | Quản lý Môn học + Số tín chỉ |
| 6 | TuyenSinh | TK_XETTUYEN, HSO_XETTUYEN, PT_XETTUYEN | Workflow xét tuyển |
| 7 | SinhVien | SinhVien | Quản lý Sinh viên |
| 8 | HocTap | KQ_HocTap | Nhập điểm + Tính GPA |
| 9 | TotNghiep | TotNghiep | Xét tốt nghiệp + Xếp loại |
| 10 | ThongBao | ThongBao, TB_NguoiNhan | Admin gửi → SV nhận |
| 11 | QuanTri | QuanTri | Dashboard + actions cho admin |
| 12 | Core | BaseModel, BaseService, BaseLivewire | Base classes dùng chung |

## Luồng nghiệp vụ chính

```
[Thí sinh] Register → Tạo TK_XETTUYEN + HSO_XETTUYEN
                     ↓
              Nộp PT_XetTuyen (chọn ngành, điểm)
                     ↓
              [Admin] Duyệt / Từ chối
                     ↓
              [Đậu] → Auto tạo SinhVien mới
                     ↓
              [SV] Xem điểm → GPA tự động
                     ↓
              [Admin] Xét tốt nghiệp → Xếp loại tự động
                     ↓
              [Admin] Gửi thông báo → [SV] Nhận
```

## 3 Auth Guards

| Guard | Model | Login field | Sử dụng |
|-------|-------|-------------|---------|
| `candidate` | TKXetTuyen | Email | Thí sinh đăng ký xét tuyển |
| `student` | SinhVien | MaSV | Sinh viên đã nhập học |
| `admin` | QuanTri | TenDN | Quản trị viên |

## Công nghệ sử dụng

| Layer | Technology |
|-------|-----------|
| Backend | Laravel 11 (PHP 8.2+) |
| Frontend | Laravel Livewire 3 + TailwindCSS |
| Database | MySQL 8.0 |
| Auth | Laravel Sanctum (3 guards) |
| Validation | Livewire inline validation |
| Migrations | Laravel Migrations |

## Cài đặt

```bash
composer install
cp .env.example .env
php artisan key:generate
php artisan migrate
php artisan db:seed
php artisan serve
```

**Tài khoản mặc định:**
- Admin: `admin` / `admin123`
- Khoa: CN, KT, NN, DL
- Ngành: CNTT, KHMT, KTPM, MKT, QTKD, TA, DLKS
- Lớp: CNTT-K63A, KHMT-K63A, ...
- Môn học: CSLT, CTDL, Mạng, CSDL, ...

## Cấu trúc thư mục

```
app/Modules/
├── Auth/         # Login, Register, Dashboard cho 3 role
├── Core/          # BaseModel, BaseService, BaseLivewire
├── Khoa/          # CRUD Khoa
├── Nganh/         # CRUD Ngành
├── Lop/           # CRUD Lớp
├── MonHoc/        # CRUD Môn học
├── SinhVien/      # CRUD + Profile Sinh viên
├── TuyenSinh/     # Workflow xét tuyển
├── HocTap/        # Nhập điểm + GPA
├── TotNghiep/     # Xét tốt nghiệp + Xếp loại
├── ThongBao/      # Gửi / Nhận thông báo
└── QuanTri/       # Dashboard Admin
```

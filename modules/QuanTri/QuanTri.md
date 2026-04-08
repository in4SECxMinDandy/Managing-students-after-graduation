# Module QuanTri

## Entity

| Field | Type | Rules |
|-------|------|-------|
| MaAdmin | VARCHAR(4) | PK |
| TenDN | VARCHAR(20) | UNIQUE, NOT NULL |
| MatKhau | VARCHAR(255) | NOT NULL |

## Business Rules

- QuanTri là người quản lý toàn bộ hệ thống
- Có 3 guard: `candidate`, `student`, `admin` (trong auth.php)
- QuanTri có quyền:
  - CRUD Khoa, Nganh, Lop, MonHoc
  - Duyệt xét tuyển (TuyenSinh)
  - Nhập điểm (HocTap)
  - Xét tốt nghiệp (TotNghiep)
  - Gửi thông báo (ThongBao)

## Tài khoản mặc định

| MaAdmin | TenDN | MatKhau |
|--------|-------|---------|
| AD01 | admin | admin123 |

## Files

- `app/Modules/QuanTri/Models/QuanTri.php`
- `app/Modules/QuanTri/Http/Livewire/AdminDashboard.php`
- `resources/views/livewire/quan-tri/dashboard.blade.php`

## Dashboard Admin

Trang dashboard hiển thị các module quản lý:
- Khoa, Ngành, Lớp, Môn học
- Xét tuyển, Sinh viên, Học tập
- Tốt nghiệp, Thông báo

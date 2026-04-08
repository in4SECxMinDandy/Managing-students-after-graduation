# Module Auth

## Entities

| Entity | Bảng | Khóa chính |
|--------|------|-----------|
| TKXetTuyen | tk_xet_tuyen | MaTK |
| QuanTri | quan_tri | MaAdmin |
| SinhVien | sinh_vien | MaSV |

## Business Rules

### 3 Actor Roles

| Actor | Guard | Login Field | Password Field |
|-------|-------|------------|----------------|
| Thí sinh xét tuyển | `candidate` | Email | MatKhau |
| Sinh viên đã nhập học | `student` | MaSV | MatKhau |
| Quản trị viên | `admin` | TenDN | MatKhau |

### Quy tắc đăng ký

- Thí sinh: `email` phải định dạng hợp lệ, `CCCD` 10 số, `SDT` 10 số
- Admin: chỉ được tạo bởi seeder hoặc admin khác
- Sinh viên: được tạo tự động khi admin duyệt xét tuyển

### Quy tắc đăng nhập

- Candidate: `email` → guard `candidate`
- Student: `MaSV` → guard `student`
- Admin: `TenDN` → guard `admin`
- Mật khẩu lưu plain text (cần băm trong production)

## Files

- `app/Modules/Auth/Services/AuthService.php` — login/logout/guard helpers
- `app/Modules/Auth/Http/Livewire/CandidateLogin.php`
- `app/Modules/Auth/Http/Livewire/CandidateRegister.php`
- `app/Modules/Auth/Http/Livewire/StudentLogin.php`
- `app/Modules/Auth/Http/Livewire/AdminLogin.php`
- `app/Modules/Auth/Http/Livewire/CandidateDashboard.php`
- `app/Modules/Auth/Http/Livewire/StudentDashboard.php`
- `app/Modules/Auth/Http/Livewire/AdminDashboard.php`
- `resources/views/livewire/auth/*.blade.php`

## Routes

```
/candidate/login   → CandidateLogin
/candidate/register → CandidateRegister
/candidate/dashboard → CandidateDashboard
/student/login     → StudentLogin
/student/dashboard → StudentDashboard
/admin/login      → AdminLogin
/admin/dashboard   → AdminDashboard
/logout           → POST destroy session
```

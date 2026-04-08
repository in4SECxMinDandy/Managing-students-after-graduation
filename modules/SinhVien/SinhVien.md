# Module SinhVien

## Entity

| Field | Type | Rules |
|-------|------|-------|
| MaSV | VARCHAR(10) | PK, auto-gen |
| HoTen | VARCHAR(100) | NOT NULL |
| NgaySinh | DATE | NOT NULL |
| Email | VARCHAR(100) | UNIQUE |
| MatKhau | VARCHAR(255) | NOT NULL |
| MaLop | VARCHAR(11) | FK → Lop (nullable) |
| MaHSO | VARCHAR(5) | FK → HSO_XETTUYEN (nullable) |

## Business Rules

- MaSV: auto-gen format `SV` + năm (2 số) + số thứ tự (8 số)
- NgaySinh: không được là ngày trong tương lai
- Email: unique
- SinhVien được tạo tự động khi admin duyệt PT_XetTuyen (TrangThai = "Đậu")
- Lop nullable → sinh viên chưa xếp lớp vẫn tồn tại

## Workflow tạo SinhVien

```
1. Thí sinh đăng ký → TK_XETTUYEN + HSO_XETTUYEN
2. Thí sinh nộp PT_XetTuyen (MaNganh, Diem, PhuongThuc)
3. Admin duyệt → TuyenSinhService::approveApplication()
   → autoCreateSinhVien() được gọi
   → SinhVien mới được tạo với HoTen, Email từ HSO
```

## Files

- `app/Modules/SinhVien/Models/SinhVien.php`
- `app/Modules/SinhVien/Services/SinhVienService.php`
- `app/Modules/SinhVien/Http/Livewire/SinhVienIndex.php`
- `app/Modules/SinhVien/Http/Livewire/SinhVienProfile.php`
- `app/Modules/SinhVien/Resources/SinhVienResource.php`

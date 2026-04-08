# Module TuyenSinh

## Entities

| Entity | Bảng | Khóa chính | Notes |
|--------|------|-----------|-------|
| TKXetTuyen | tk_xet_tuyen | MaTK | Tài khoản thí sinh |
| HSOXetTuyen | hso_xet_tuyen | MaHSO | Hồ sơ cá nhân |
| PTXetTuyen | pt_xet_tuyen | MaPTXT | Phiếu đăng ký xét tuyển |

## PT_XetTuyen Fields

| Field | Type | Rules |
|-------|------|-------|
| MaPTXT | VARCHAR(10) | PK |
| MaHSO | VARCHAR(5) | FK → HSOXetTuyen |
| MaNganh | VARCHAR(4) | FK → Nganh |
| PhuongThuc | VARCHAR(100) | NOT NULL |
| Diem | DECIMAL(4,2) | 0.00 → 30.00 |
| TrangThai | VARCHAR(100) | DEFAULT "Chờ duyệt" |
| MaAdmin | VARCHAR(4) | FK → QuanTri (nullable) |

## Business Rules

### Trạng thái PT_XetTuyen

| Trạng thái | Giá trị | Mô tả |
|-------------|---------|--------|
| Chờ duyệt | `Chờ duyệt` | Mặc định khi nộp |
| Đậu | `Đậu` | Admin duyệt |
| Rớt | `Rớt` | Admin từ chối |

### Validation

- Email TK_XETTUYEN: format hợp lệ, unique
- CCCD: đúng 10 số, unique
- SDT: đúng 10 số, unique
- Diem: 0.00 → 30.00

### Workflow

```
1. Candidate Register → TK_XETTUYEN + HSO_XETTUYEN
2. Candidate Apply → PT_XETTUYEN (TrangThai = "Chờ duyệt")
3. Admin AdmissionList → Duyệt / Từ chối
   - Duyệt: TrangThai = "Đậu" → autoCreateSinhVien()
   - Từ chối: TrangThai = "Rớt"
```

## Files

- `app/Modules/TuyenSinh/Models/TKXetTuyen.php`
- `app/Modules/TuyenSinh/Models/HSOXetTuyen.php`
- `app/Modules/TuyenSinh/Models/PTXetTuyen.php`
- `app/Modules/TuyenSinh/Services/TuyenSinhService.php`
- Candidate Livewire: Register, Apply, Status
- Admin Livewire: AdmissionList

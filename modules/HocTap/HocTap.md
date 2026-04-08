# Module HocTap

## Entity

| Field | Type | Rules |
|-------|------|-------|
| MaSV | VARCHAR(10) | PK, FK → SinhVien |
| MaMH | VARCHAR(7) | PK, FK → MonHoc |
| Diem | DECIMAL(4,2) | 0.00 → 10.00 |

> **Composite Primary Key**: (MaSV, MaMH) — mỗi sinh viên không học trùng môn

## Business Rules

### GPA Calculation (Weighted Average)

```
GPA (thang 4) = (Σ(Diem × SoTinChi)) / Σ(SoTinChi) / 2.5
```

**Ví dụ:**
- Môn A: Điểm 8.0, 3 tín chỉ → 8.0 × 3 = 24
- Môn B: Điểm 7.0, 4 tín chỉ → 7.0 × 4 = 28
- Tổng: 52 / 7 / 2.5 = **2.97 GPA**

### Diem quy đổi thang 10

- Diem nhập: 0.00 → 10.00
- GPA output: 0.00 → 4.00

## Files

- `app/Modules/HocTap/Models/KQHocTap.php`
- `app/Modules/HocTap/Services/HocTapService.php`
- `app/Modules/HocTap/Http/Livewire/HocTapIndex.php` (admin nhập điểm)
- `app/Modules/HocTap/Http/Livewire/Transcript.php` (SV xem bảng điểm + GPA)

# Module TotNghiep

## Entity

| Field | Type | Rules |
|-------|------|-------|
| MaSV | VARCHAR(10) | PK, FK → SinhVien |
| GPA | DECIMAL(4,2) | 0.00 → 4.00 |
| XepLoai | VARCHAR(20) | NOT NULL |

## Business Rules

### Xếp loại tốt nghiệp (tự động theo GPA)

| GPA | Xếp loại |
|-----|-----------|
| ≥ 3.60 | Xuất sắc |
| ≥ 3.20 | Giỏi |
| ≥ 2.50 | Khá |
| ≥ 2.00 | Trung bình |
| < 2.00 | Yếu |

### Logic xếp loại (in `TotNghiep::tinhXepLoai()`)

```php
return match (true) {
    $gpa >= 3.60 => self::XUAT_SAC,
    $gpa >= 3.20 => self::GIOI,
    $gpa >= 2.50 => self::KHA,
    $gpa >= 2.00 => self::TRUNG_BINH,
    default      => self::YEU,
};
```

### Xét tốt nghiệp

- Admin gọi `TotNghiepService::xetTotNghiep(MaSV)`
- Service gọi `HocTapService::tinhGPA(MaSV)` → lấy GPA mới nhất
- Tự động xác định XepLoai
- `updateOrCreate`: tạo mới hoặc cập nhật nếu đã tồn tại

## Files

- `app/Modules/TotNghiep/Models/TotNghiep.php`
- `app/Modules/TotNghiep/Services/TotNghiepService.php`
- `app/Modules/TotNghiep/Http/Livewire/TotNghiepIndex.php` (admin xét TN)
- `app/Modules/TotNghiep/Http/Livewire/Result.php` (SV xem kết quả)

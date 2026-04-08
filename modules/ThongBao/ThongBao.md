# Module ThongBao

## Entities

| Entity | Bảng | Khóa chính | Notes |
|--------|------|-----------|-------|
| ThongBao | thong_bao | MaTB | Thông báo |
| TBNguoiNhan | tb_nguoi_nhan | id (auto) | Bảng trung gian |

## Business Rules

### Admin gửi thông báo

- Chọn đối tượng nhận:
  - `all`: tất cả SinhVien
  - `khoa`: theo MaKhoa (lọc qua Lop → Nganh → Khoa)
  - `nganh`: theo MaNganh (lọc qua Lop → Nganh)
  - `lop`: theo MaLop
- Mỗi SinhVien được tạo 1 record trong TB_NguoiNhan

### Trạng thái đọc

| Trường | Type | Mô tả |
|--------|------|--------|
| TrangThaiDoc | BOOLEAN | 0 = chưa đọc, 1 = đã đọc |
| ThoiGianDoc | DATE | Thời điểm đọc (nullable) |

### Logic gửi (trong transaction)

```php
// 1. Tạo ThongBao
$thongBao = ThongBao::create([...]):

// 2. Lọc SinhVien theo loai
$sinhViens = match ($loai) {
    'khoa' => SV theo Khoa,
    'nganh' => SV theo Nganh,
    'lop' => SV theo Lop,
    default => Tất cả SV,
};

// 3. Tạo TB_NguoiNhan cho từng SV
foreach ($sinhViens as $sv) {
    TBNguoiNhan::create([...]);
}
```

## Files

- `app/Modules/ThongBao/Models/ThongBao.php`
- `app/Modules/ThongBao/Models/TBNguoiNhan.php`
- `app/Modules/ThongBao/Services/ThongBaoService.php`
- Admin Livewire: ThongBaoCreate, ThongBaoList
- Student Livewire: ThongBaoList

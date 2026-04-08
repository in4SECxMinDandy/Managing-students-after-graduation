# Module Nganh

## Entity

| Field | Type | Rules |
|-------|------|-------|
| MaNganh | VARCHAR(4) | PK, size=4, unique |
| TenNganh | VARCHAR(100) | NOT NULL |
| MaKhoa | VARCHAR(2) | FK → Khoa.MaKhoa |

## Business Rules

- MaNganh: đúng 4 ký tự (VD: CNTT, KHMT, MKT)
- FK: Nganh belongsTo Khoa
- Khoa có nhiều Nganh (1:N)

## Files

- `app/Modules/Nganh/Models/Nganh.php`
- `app/Modules/Nganh/Services/NganhService.php`
- `app/Modules/Nganh/Http/Livewire/NganhIndex.php`
- `app/Modules/Nganh/Http/Livewire/NganhCreate.php`
- `app/Modules/Nganh/Http/Livewire/NganhEdit.php`

## Seeder Data

| MaNganh | TenNganh | MaKhoa |
|---------|----------|--------|
| CNTT | Công nghệ thông tin | CN |
| KHMT | Khoa học máy tính | CN |
| KTPM | Kỹ thuật phần mềm | CN |
| MKT | Marketing | KT |
| QTKD | Quản trị kinh doanh | KT |
| TA | Tiếng Anh | NN |
| DLKS | Du lịch và Khách sạn | DL |

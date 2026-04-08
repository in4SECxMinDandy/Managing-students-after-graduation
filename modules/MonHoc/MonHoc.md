# Module MonHoc

## Entity

| Field | Type | Rules |
|-------|------|-------|
| MaMH | VARCHAR(7) | PK, size=7, unique |
| TenMH | VARCHAR(100) | NOT NULL |
| SoTinChi | INT | NOT NULL, > 0 |

## Business Rules

- MaMH: 7 ký tự (VD: CTRR001)
- SoTinChi: phải > 0
- SoTinChi dùng để tính GPA (weighted average)

## Files

- `app/Modules/MonHoc/Models/MonHoc.php`
- `app/Modules/MonHoc/Services/MonHocService.php`
- `app/Modules/MonHoc/Http/Livewire/MonHocIndex.php`
- `app/Modules/MonHoc/Http/Livewire/MonHocCreate.php`
- `app/Modules/MonHoc/Http/Livewire/MonHocEdit.php`

## Seeder Data

| MaMH | TenMH | SoTinChi |
|------|-------|---------|
| CTRR001 | Cơ sở lập trình | 3 |
| CTRR002 | Cấu trúc dữ liệu và giải thuật | 4 |
| CTRR003 | Mạng máy tính | 3 |
| CTRR004 | Cơ sở dữ liệu | 3 |
| CTRR005 | Lập trình hướng đối tượng | 3 |
| CTRR006 | Toán cao cấp A1 | 4 |
| CTRR007 | Xác suất thống kê | 3 |
| CTRR008 | Tiếng Anh chuyên ngành | 3 |

# Module Lop

## Entity

| Field | Type | Rules |
|-------|------|-------|
| MaLop | VARCHAR(11) | PK, size=11, unique |
| TenLop | VARCHAR(100) | NOT NULL, unique |
| MaNganh | VARCHAR(4) | FK → Nganh.MaNganh |

## Business Rules

- MaLop: format 11 ký tự (VD: CNTT-K63A)
- FK: Lop belongsTo Nganh
- Nganh có nhiều Lop (1:N)

## Files

- `app/Modules/Lop/Models/Lop.php`
- `app/Modules/Lop/Services/LopService.php`
- `app/Modules/Lop/Http/Livewire/LopIndex.php`
- `app/Modules/Lop/Http/Livewire/LopCreate.php`
- `app/Modules/Lop/Http/Livewire/LopEdit.php`

## Seeder Data

| MaLop | TenLop | MaNganh |
|-------|--------|---------|
| CNTT-K63A | CNTT K63 A | CNTT |
| CNTT-K63B | CNTT K63 B | CNTT |
| KHMT-K63A | KHMT K63 A | KHMT |
| MKT-K63A | Marketing K63 A | MKT |
| QTKD-K63A | QTKD K63 A | QTKD |

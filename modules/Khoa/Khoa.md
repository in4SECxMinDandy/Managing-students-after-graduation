# Module Khoa

## Entity

| Field | Type | Rules |
|-------|------|-------|
| MaKhoa | VARCHAR(2) | PK, size=2, unique |
| TenKhoa | VARCHAR(100) | NOT NULL, unique |

## Business Rules

- MaKhoa: đúng 2 ký tự (VD: CN, KT, NN, DL)
- TenKhoa: unique, NOT NULL
- FK: Khoa có nhiều Nganh (1:N)

## Files

- `app/Modules/Khoa/Models/Khoa.php`
- `app/Modules/Khoa/Services/KhoaService.php`
- `app/Modules/Khoa/Http/Livewire/KhoaIndex.php`
- `app/Modules/Khoa/Http/Livewire/KhoaCreate.php`
- `app/Modules/Khoa/Http/Livewire/KhoaEdit.php`
- `resources/views/livewire/khoa/*.blade.php`

## Seeder Data

| MaKhoa | TenKhoa |
|--------|---------|
| CN | Công nghệ thông tin |
| KT | Kinh tế |
| NN | Ngôn ngữ |
| DL | Du lịch |

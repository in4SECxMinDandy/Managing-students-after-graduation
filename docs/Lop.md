# Lop - Quản lý Lớp

## Mô tả

Module **Lop** quản lý danh sách lớp học thuộc các Ngành.

## Database Schema

```sql
CREATE TABLE Lop (
    MaLop VARCHAR(11) PRIMARY KEY,
    TenLop VARCHAR(100) NOT NULL UNIQUE,
    MaNganh VARCHAR(4),
    FOREIGN KEY(MaNganh) REFERENCES Nganh(MaNganh)
);
```

## Relationships

```
Nganh (1) ──── (N) Lop ──── (N) SinhVien
```

## API Endpoints

| Method | Endpoint | Mô tả | Auth |
|--------|----------|--------|------|
| GET | `/api/lop/` | Danh sách lớp | No |
| GET | `/api/lop/<ma_lop>` | Chi tiết lớp | No |
| POST | `/api/lop/` | Tạo lớp | Admin |
| PUT | `/api/lop/<ma_lop>` | Cập nhật lớp | Admin |
| DELETE | `/api/lop/<ma_lop>` | Xóa lớp | Admin |
| GET | `/api/lop/<ma_lop>/sinh-vien` | SV thuộc lớp | No |

## Business Rules

- `MaLop`: Unique, PRIMARY KEY
- `TenLop`: Unique, NOT NULL
- `MaNganh`: FOREIGN KEY → Nganh

## Dependencies

- Phụ thuộc: Nganh
- Được phụ thuộc bởi: SinhVien

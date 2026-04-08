# Nganh - Quản lý Ngành

## Mô tả

Module **Nganh** quản lý danh sách ngành học thuộc các Khoa.

## Database Schema

```sql
CREATE TABLE Nganh (
    MaNganh VARCHAR(4) PRIMARY KEY,
    TenNganh VARCHAR(100) NOT NULL,
    MaKhoa VARCHAR(2),
    FOREIGN KEY(MaKhoa) REFERENCES Khoa(MaKhoa)
);
```

## Relationships

```
Khoa (1) ──── (N) Nganh ──── (N) Lop
```

## API Endpoints

| Method | Endpoint | Mô tả | Auth |
|--------|----------|--------|------|
| GET | `/api/nganh/` | Danh sách ngành | No |
| GET | `/api/nganh/<ma_nganh>` | Chi tiết ngành | No |
| POST | `/api/nganh/` | Tạo ngành | Admin |
| PUT | `/api/nganh/<ma_nganh>` | Cập nhật ngành | Admin |
| DELETE | `/api/nganh/<ma_nganh>` | Xóa ngành | Admin |
| GET | `/api/nganh/<ma_nganh>/lop` | Lớp thuộc ngành | No |

## Business Rules

- `MaNganh`: Độ dài 4 ký tự, unique
- `TenNganh`: NOT NULL
- `MaKhoa`: FOREIGN KEY → Khoa

## Dependencies

- Phụ thuộc: Khoa
- Được phụ thuộc bởi: Lop, PT_XETTUYEN

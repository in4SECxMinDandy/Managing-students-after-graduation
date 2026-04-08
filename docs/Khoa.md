# Khoa - Quản lý Khoa

## Mô tả

Module **Khoa** quản lý danh sách các Khoa/Bộ môn trong trường đại học.

## Database Schema

```sql
CREATE TABLE Khoa (
    MaKhoa VARCHAR(2) PRIMARY KEY,
    TenKhoa VARCHAR(100) NOT NULL UNIQUE
);
```

## Relationships

```
Khoa (1) ──── (N) Nganh
```

## API Endpoints

| Method | Endpoint | Mô tả | Auth |
|--------|----------|--------|------|
| GET | `/api/khoa/` | Danh sách khoa | No |
| GET | `/api/khoa/<ma_khoa>` | Chi tiết khoa | No |
| POST | `/api/khoa/` | Tạo khoa | Admin |
| PUT | `/api/khoa/<ma_khoa>` | Cập nhật khoa | Admin |
| DELETE | `/api/khoa/<ma_khoa>` | Xóa khoa | Admin |
| GET | `/api/khoa/<ma_khoa>/nganh` | Ngành thuộc khoa | No |

## Business Rules

- `MaKhoa`: Độ dài 2 ký tự, unique, PRIMARY KEY
- `TenKhoa`: Unique, NOT NULL

## Example Usage

```python
# Get all khoa
result = api.get("/khoa/")

# Create khoa (admin)
result = api.post("/khoa/", {
    "MaKhoa": "KT",
    "TenKhoa": "Khoa Kinh tế"
})
```

## Dependencies

- Không phụ thuộc module khác
- Được phụ thuộc bởi: Nganh

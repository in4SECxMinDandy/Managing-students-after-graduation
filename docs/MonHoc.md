# MonHoc - Quản lý Môn học

## Mô tả

Module **MonHoc** quản lý danh sách môn học và số tín chỉ tương ứng.

## Database Schema

```sql
CREATE TABLE MonHoc (
    MaMH VARCHAR(7) PRIMARY KEY,
    TenMH VARCHAR(100) NOT NULL,
    SoTinChi INT NOT NULL CHECK (SoTinChi > 0)
);
```

## Relationships

```
MonHoc (1) ──── (N) KQ_HocTap
```

## API Endpoints

| Method | Endpoint | Mô tả | Auth |
|--------|----------|--------|------|
| GET | `/api/mon-hoc/` | Danh sách môn học | No |
| GET | `/api/mon-hoc/<ma_mh>` | Chi tiết môn học | No |
| POST | `/api/mon-hoc/` | Tạo môn học | Admin |
| PUT | `/api/mon-hoc/<ma_mh>` | Cập nhật môn học | Admin |
| DELETE | `/api/mon-hoc/<ma_mh>` | Xóa môn học | Admin |

## Business Rules

- `MaMH`: Độ dài 7 ký tự, unique
- `TenMH`: NOT NULL
- `SoTinChi`: > 0, dùng để tính GPA

## Example Usage

```python
# Get all mon hoc
result = api.get("/mon-hoc/")

# Create mon hoc (admin)
result = api.post("/mon-hoc/", {
    "MaMH": "TH03001",
    "TenMH": "Toán cao cấp",
    "SoTinChi": 3
})
```

## Dependencies

- Không phụ thuộc module khác
- Được phụ thuộc bởi: KQHocTap (tính GPA)

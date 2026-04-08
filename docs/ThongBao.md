# ThongBao - Quản lý Thông báo

## Mô tả

Module **ThongBao** cho phép admin gửi thông báo đến sinh viên.

## Database Schema

### ThongBao

```sql
CREATE TABLE ThongBao (
    MaTB VARCHAR(100) PRIMARY KEY,
    NoiDung VARCHAR(100) NOT NULL,
    NgayGui DATE DEFAULT CURRENT_DATE,
    MaAdmin VARCHAR(4),
    FOREIGN KEY(MaAdmin) REFERENCES QuanTri(MaAdmin)
);
```

### TB_NguoiNhan

```sql
CREATE TABLE TB_NguoiNhan (
    MaTBNN INT PRIMARY KEY AUTO_INCREMENT,
    MaTB VARCHAR(100),
    MaSV VARCHAR(10),
    TrangThaiDoc TINYINT(1) DEFAULT 0,
    ThoiGianDoc DATE,
    FOREIGN KEY(MaTB) REFERENCES ThongBao(MaTB),
    FOREIGN KEY(MaSV) REFERENCES SinhVien(MaSV)
);
```

## Relationships

```
QuanTri (1) ──── (N) ThongBao ──── (N) TB_NguoiNhan ──── (1) SinhVien
```

## Gửi thông báo

Admin có thể gửi đến:

1. **Tất cả sinh viên**: `gui_den = "all"`
2. **Theo lớp**: `gui_den = "lop"`, `ma_target = ma_lop`
3. **Theo ngành**: `gui_den = "nganh"`, `ma_target = ma_nganh`

## API Endpoints

### Sinh viên

| Method | Endpoint | Mô tả | Auth |
|--------|----------|--------|------|
| GET | `/api/thong-bao/my` | Thông báo của tôi | Student |
| POST | `/api/thong-bao/read/<ma_tb>` | Đánh dấu đã đọc | Student |

### Admin

| Method | Endpoint | Mô tả | Auth |
|--------|----------|--------|------|
| GET | `/api/thong-bao/` | Danh sách TB | Admin |
| POST | `/api/thong-bao/` | Tạo & gửi TB | Admin |
| DELETE | `/api/thong-bao/<ma_tb>` | Xóa TB | Admin |
| GET | `/api/thong-bao/<ma_tb>/details` | Chi tiết TB | Admin |

## Business Rules

- `MaTB`: Auto-generate (UUID)
- `NgayGui`: Auto-set = CURRENT_DATE
- `TrangThaiDoc`: 0 = Chưa đọc, 1 = Đã đọt
- `ThoiGianDoc`: Auto-set khi sinh viên đọc

## Dependencies

- Phụ thuộc: QuanTri
- Tạo: TB_NguoiNhan (khi gửi)

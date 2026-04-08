# SinhVien - Quản lý Sinh viên

## Mô tả

Module **SinhVien** quản lý thông tin sinh viên đã trúng tuyển.

## Database Schema

```sql
CREATE TABLE SinhVien (
    MaSV VARCHAR(10) PRIMARY KEY,
    HoTen VARCHAR(100) NOT NULL,
    NgaySinh DATE NOT NULL,
    Email VARCHAR(100) NOT NULL UNIQUE,
    MatKhau VARCHAR(255) NOT NULL,
    MaLop VARCHAR(11),
    MaHSO VARCHAR(5),
    FOREIGN KEY (MaLop) REFERENCES Lop(MaLop),
    FOREIGN KEY (MaHSO) REFERENCES HSO_XETTUYEN(MaHSO)
);
```

## Relationships

```
Lop (1) ──── (N) SinhVien ──── (1) HSO_XETTUYEN
  │
  └── (1) SinhVien ──── (N) KQ_HocTap
  │
  └── (1) SinhVien ──── (1) TotNghiep
  │
  └── (1) SinhVien ──── (N) TB_NguoiNhan
```

## MaSV Format

```
SVyyXXXXXXXX
├── SV: Prefix (Sinh Viên)
├── yy: 2 số cuối năm (VD: 25 = 2025)
└── XXXXXXXX: 8 số random
```

## API Endpoints

| Method | Endpoint | Mô tả | Auth |
|--------|----------|--------|------|
| GET | `/api/sinh-vien/` | Danh sách SV | Admin |
| GET | `/api/sinh-vien/<ma_sv>` | Chi tiết SV | Admin/SV* |
| POST | `/api/sinh-vien/` | Tạo SV | Admin |
| PUT | `/api/sinh-vien/<ma_sv>` | Cập nhật SV | Admin/SV* |
| DELETE | `/api/sinh-vien/<ma_sv>` | Xóa SV | Admin |
| GET | `/api/sinh-vien/search?q=` | Tìm kiếm | Admin |

*Sinh viên chỉ xem/sửa thông tin của mình

## Business Rules

- `MaSV`: Format SVyyXXXXXXXX
- `Email`: Unique
- `NgaySinh`: Không future
- `MatKhau`: Min 6 ký tự, hash bằng werkzeug

## Dependencies

- Phụ thuộc: Lop, HSO_XETTUYEN
- Được phụ thuộc bởi: KQHocTap, TotNghiep, TB_NguoiNhan

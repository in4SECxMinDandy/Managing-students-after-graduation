# HocTap - Kết quả Học tập

## Mô tả

Module **HocTap** quản lý điểm số và tính GPA cho sinh viên.

## Database Schema

```sql
CREATE TABLE KQ_HocTap (
    MaSV VARCHAR(10),
    MaMH VARCHAR(7),
    Diem DECIMAL(4,2) NOT NULL,
    FOREIGN KEY(MaSV) REFERENCES SinhVien(MaSV),
    FOREIGN KEY(MaMH) REFERENCES MonHoc(MaMH),
    PRIMARY KEY(MaSV, MaMH)
);
```

## Relationships

```
SinhVien (1) ──── (N) KQ_HocTap ──── (1) MonHoc
```

## GPA Calculation

### Công thức

```
GPA (thang 10) = Σ(Diem × SoTinChi) / Σ(SoTinChi)
GPA (thang 4) = GPA (thang 10) / 2.5
```

### Ví dụ

| Môn | Điểm | Số TC | Điểm × TC |
|-----|------|-------|-----------|
| Toán | 8.0 | 3 | 24.0 |
| Lý | 7.5 | 2 | 15.0 |
| Hóa | 9.0 | 2 | 18.0 |
| **Tổng** | - | 7 | 57.0 |

```
GPA (thang 10) = 57.0 / 7 = 8.14
GPA (thang 4) = 8.14 / 2.5 = 3.26
```

## API Endpoints

| Method | Endpoint | Mô tả | Auth |
|--------|----------|--------|------|
| GET | `/api/hoc-tap/diem/<ma_sv>` | Bảng điểm | Admin/SV* |
| POST | `/api/hoc-tap/diem` | Nhập điểm | Admin |
| POST | `/api/hoc-tap/diem/batch` | Nhập nhiều điểm | Admin |
| DELETE | `/api/hoc-tap/diem/<ma_sv>/<ma_mh>` | Xóa điểm | Admin |
| GET | `/api/hoc-tap/gpa/<ma_sv>` | Tính GPA | Admin/SV* |
| GET | `/api/hoc-tap/mon-hoc` | Danh sách MH | No |

*SV chỉ xem điểm của mình

## Business Rules

- `Diem`: 0-10
- Composite PK: (MaSV, MaMH) - mỗi SV chỉ có 1 điểm cho mỗi môn
- Upsert: Nếu điểm đã tồn tại → UPDATE, ngược lại → INSERT

## Dependencies

- Phụ thuộc: SinhVien, MonHoc
- Được phụ thuộc bởi: TotNghiep (dùng GPA để xếp loại)

# TotNghiep - Xét Tốt nghiệp

## Mô tả

Module **TotNghiep** xử lý xét tốt nghiệp và xếp loại cho sinh viên.

## Database Schema

```sql
CREATE TABLE TotNghiep (
    MaSV VARCHAR(10) PRIMARY KEY,
    GPA DECIMAL(4,2) NOT NULL CHECK (GPA >=0 AND GPA <=4.0),
    XepLoai VARCHAR(20) NOT NULL,
    FOREIGN KEY(MaSV) REFERENCES SinhVien(MaSV)
);
```

## Xếp loại tốt nghiệp

| GPA (thang 4) | Xếp loại | Màu |
|---------------|----------|-----|
| ≥ 3.60 | Xuất sắc | 🟢 Gold |
| ≥ 3.20 | Giỏi | 🔵 Blue |
| ≥ 2.50 | Khá | 🟡 Yellow |
| ≥ 2.00 | Trung bình | 🟠 Orange |
| < 2.00 | Yếu | 🔴 Red |

## Calculation Flow

```
┌─────────────────────────────────────────────────────────────┐
│                  TỐT NGHIỆP WORKFLOW                        │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  1. Sinh viên hoàn thành học tập                            │
│                                                              │
│  2. Admin nhập điểm cho tất cả môn                          │
│     → KQ_HocTap                                             │
│                                                              │
│  3. Tính GPA                                                │
│     GPA = Σ(Diem × SoTinChi) / Σ(SoTinChi) / 2.5            │
│                                                              │
│  4. Xác định xếp loại                                       │
│     GPA ≥ 3.60 → "Xuất sắc"                                 │
│     GPA ≥ 3.20 → "Giỏi"                                     │
│     GPA ≥ 2.50 → "Khá"                                      │
│     GPA ≥ 2.00 → "Trung bình"                               │
│     GPA < 2.00 → "Yếu"                                      │
│                                                              │
│  5. Cập nhật bảng TotNghiep                                 │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## API Endpoints

| Method | Endpoint | Mô tả | Auth |
|--------|----------|--------|------|
| GET | `/api/tot-nghiep/check/<ma_sv>` | Xét tốt nghiệp | Admin/SV* |
| GET | `/api/tot-nghiep/status/<ma_sv>` | Trạng thái TN | Admin/SV* |
| GET | `/api/tot-nghiep/all` | Danh sách TN | Admin |
| GET | `/api/tot-nghiep/xep-loai-stats` | Thống kê XL | Admin |

*SV chỉ xem thông tin của mình

## Business Rules

- `GPA`: 0.00 - 4.00
- `XepLoai`: Tự động tính từ GPA
- Upsert: Nếu đã xét → UPDATE GPA mới

## Dependencies

- Phụ thuộc: SinhVien, KQHocTap, MonHoc

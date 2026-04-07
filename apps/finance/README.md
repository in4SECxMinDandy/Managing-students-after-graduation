# Finance Module

## Mô tả

Module quản lý tài chính: đơn giá tín chỉ và học phí.

## API Endpoints

### Đơn giá tín chỉ
- `GET /finance/tuition-rates` — Danh sách đơn giá
- `POST /finance/tuition-rates` — Tạo đơn giá mới
- `PUT /finance/tuition-rates/{ma_dg}` — Cập nhật đơn giá

### Học phí
- `GET /finance/tuitions` — Danh sách học phí
- `POST /finance/tuitions` — Tạo học phí
- `PUT /finance/tuitions/{ma_hp}` — Cập nhật (đánh dấu đã đóng)

## Business Rules

| Rule | Mô tả |
|------|-------|
| BR-05 | SoTien = SoTinChi × DonGia, tự động tính khi duyệt đăng ký |

## Trạng thái học phí

| Trạng thái | Mô tả |
|------------|-------|
| `ChuaDong` | Chưa đóng |
| `DaDong` | Đã đóng |
| `DongMotPhan` | Đóng một phần |

## Vai trò được phép

Chỉ `admin` và `super_admin` được thao tác trên module này.

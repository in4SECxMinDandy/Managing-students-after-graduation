# Admissions Module

## Mô tả

Module quản lý tuyển sinh sau đại học: tài khoản xét tuyển, hồ sơ ứng tuyển, và phương thức xét tuyển.

## API Endpoints

### Tài khoản xét tuyển
- `POST /admissions/accounts` — Tạo tài khoản xét tuyển

### Hồ sơ ứng tuyển
- `GET /admissions/profiles` — Danh sách hồ sơ
- `POST /admissions/profiles` — Tạo hồ sơ
- `GET /admissions/profiles/{ma_hso}` — Chi tiết hồ sơ
- `PUT /admissions/profiles/{ma_hso}` — Cập nhật hồ sơ

### Phương thức xét tuyển
- `GET /admissions/applications` — Danh sách phương thức xét tuyển
- `POST /admissions/applications` — Tạo phương thức xét tuyển
- `PUT /admissions/applications/{ma_ptxt}` — Duyệt/từ chối

## Trạng thái xét tuyển

| Trạng thái | Mô tả |
|------------|-------|
| `ChoDuyet` | Chờ duyệt |
| `DaDuyet` | Đã duyệt |
| `TuChoi` | Từ chối |

## Vai trò được phép

Chỉ `admin` và `super_admin` được thao tác trên module này.

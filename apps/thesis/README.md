# Thesis Module

## Mô tả

Module quản lý luận văn: đăng ký đề tài, đề cương, hội đồng bảo vệ, và thù lao hội đồng.

## API Endpoints

### Luận văn
- `GET /thesis/theses` — Danh sách luận văn
- `POST /thesis/theses` — Đăng ký luận văn
- `GET /thesis/theses/{ma_lv}` — Chi tiết luận văn
- `PUT /thesis/theses/{ma_lv}` — Cập nhật (bao gồm chấm điểm)

### Đề cương luận án
- `GET /thesis/outlines` — Danh sách đề cương
- `POST /thesis/outlines` — Nộp đề cương
- `PUT /thesis/outlines/{ma_dc}` — Duyệt/từ chối đề cương

### Hội đồng bảo vệ
- `GET /thesis/committees` — Danh sách hội đồng
- `POST /thesis/committees` — Thành lập hội đồng
- `PUT /thesis/committees/{ma_hd}` — Cập nhật hội đồng

### Thành viên hội đồng
- `GET /thesis/committee-members` — Danh sách thành viên
- `POST /thesis/committee-members` — Thêm thành viên
- `PUT /thesis/committee-members/{ma_tvhd}` — Cập nhật thành viên

### Thù lao hội đồng
- `GET /thesis/stipends` — Danh sách thù lao
- `POST /thesis/stipends` — Tạo thù lao
- `PUT /thesis/stipends/{ma_tl}` — Cập nhật thù lao

## Business Rules

| Rule | Mô tả |
|------|-------|
| BR-04 | Quy đổi điểm tự động khi nhập DiemBaoVe |
| BR-07 | Hội đồng cần đủ: ChuTich, PhoChuTich, ThuKy, PhanBien1, PhanBien2 |
| BR-09 | NgayBaoVe ≥ NgayDangKy |

## Trạng thái luận văn

| Trạng thái | Mô tả |
|------------|-------|
| `ChuaBaoVe` | Chưa bảo vệ |
| `DangThucHien` | Đang thực hiện |
| `DaBaoVe` | Đã bảo vệ |
| `CanChinhSua` | Cần chỉnh sửa |
| `TuChoi` | Từ chối |

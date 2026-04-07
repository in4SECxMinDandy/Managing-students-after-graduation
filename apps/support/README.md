# Support Module

## Mô tả

Module hỗ trợ: thông báo, nghiên cứu khoa học, quy định đặc thù, tốt nghiệp, và lịch thi.

## API Endpoints

### Thông báo
- `GET /support/announcements` — Danh sách thông báo
- `POST /support/announcements` — Tạo thông báo
- `GET /support/recipients` — Người nhận thông báo
- `POST /support/recipients` — Thêm người nhận

### Nghiên cứu khoa học
- `GET /support/research` — Danh sách công trình
- `POST /support/research` — Tạo công trình NCKH
- `PUT /support/research/{ma_nckh}` — Cập nhật công trình
- `GET /support/research-authors` — Tác giả công trình
- `POST /support/research-authors` — Thêm tác giả

### Quy định đặc thù
- `GET /support/regulations` — Danh sách quy định
- `POST /support/regulations` — Tạo quy định
- `PUT /support/regulations/{ma_qd}` — Cập nhật quy định

### Tốt nghiệp
- `GET /support/graduations` — Danh sách tốt nghiệp
- `POST /support/graduations` — Ghi nhận tốt nghiệp

### Lịch thi
- `GET /support/exam-schedules` — Danh sách lịch thi
- `POST /support/exam-schedules` — Tạo lịch thi
- `PUT /support/exam-schedules/{ma_lt}` — Cập nhật lịch thi

## Business Rules

| Rule | Mô tả |
|------|-------|
| BR-08 | Xếp loại: GPA≥3.6→Xuất sắc, ≥3.2→Giỏi, ≥2.5→Khá, ≥2.0→Trung bình, <2.0→Yếu |

## Vai trò được phép

- Tạo/Sửa: `admin`, `super_admin`
- Xem: Tất cả role

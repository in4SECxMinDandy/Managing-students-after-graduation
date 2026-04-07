# Training Module

## Mô tả

Module quản lý đào tạo: lớp học phần, đăng ký học phần, phân công giảng dạy, lịch học, và kết quả học tập.

## API Endpoints

### Lớp học phần
- `GET /training/class-sections` — Danh sách lớp HP
- `POST /training/class-sections` — Tạo lớp HP
- `PUT /training/class-sections/{ma_lophp}` — Cập nhật lớp HP

### Đăng ký học phần
- `GET /training/enrollments` — Danh sách đăng ký
- `POST /training/enrollments` — Đăng ký học phần
- `PUT /training/enrollments/{ma_dk}` — Duyệt/từ chối đăng ký

### Phân công giảng dạy
- `GET /training/assignments` — Danh sách phân công
- `POST /training/assignments` — Phân công giảng viên
- `PUT /training/assignments/{ma_pc}` — Cập nhật phân công

### Lịch học
- `GET /training/schedules` — Danh sách lịch học
- `POST /training/schedules` — Tạo lịch học

### Kết quả học tập
- `GET /training/grades` — Danh sách điểm
- `POST /training/grades` — Nhập điểm
- `PUT /training/grades/{ma_sv}/{ma_mh}/{ma_hk}` — Cập nhật điểm

## Business Rules

| Rule | Mô tả |
|------|-------|
| BR-01 | SV phải hoàn thành môn tiên quyết trước khi đăng ký |
| BR-02 | SiSoHienTai ≤ SiSoToiDa mới được duyệt đăng ký |
| BR-03 | Không trùng phòng/giảng viên cùng thứ, buổi, tiết trong 1 HK |
| BR-04 | Tự động quy đổi 10→4, điểm chữ khi nhập điểm |

## Vai trò được phép

| Thao tác | Role được phép |
|----------|----------------|
| Tạo/Cập nhật lớp HP | `admin`, `super_admin`, `khoa` |
| Đăng ký học phần | Tất cả |
| Duyệt đăng ký | `admin`, `super_admin`, `khoa` |
| Nhập điểm | `admin`, `super_admin`, `khoa`, `giangvien` |

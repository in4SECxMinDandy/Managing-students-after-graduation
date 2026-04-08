# TuyenSinh - Quản lý Tuyển sinh

## Mô tả

Module **TuyenSinh** xử lý quy trình tuyển sinh từ đăng ký đến duyệt đơn.

## Database Schema

### TK_XETTUYEN (Tài khoản thí sinh)

```sql
CREATE TABLE TK_XETTUYEN (
    MaTK VARCHAR(4) PRIMARY KEY,
    Email VARCHAR(30) NOT NULL UNIQUE CHECK (Email LIKE '%@gmail.com'),
    MatKhau VARCHAR(255) NOT NULL
);
```

### HSO_XETTUYEN (Hồ sơ thí sinh)

```sql
CREATE TABLE HSO_XETTUYEN (
    MaHSO VARCHAR(5) PRIMARY KEY,
    MaTK VARCHAR(4),
    HoTen VARCHAR(100) NOT NULL,
    CCCD VARCHAR(10) NOT NULL UNIQUE,
    SDT VARCHAR(10) NOT NULL UNIQUE,
    FOREIGN KEY(MaTK) REFERENCES TK_XETTUYEN(MaTK)
);
```

### PT_XETTUYEN (Phiếu đăng ký xét tuyển)

```sql
CREATE TABLE PT_XetTuyen (
    MaPTXT VARCHAR(10) PRIMARY KEY,
    MaNganh VARCHAR(4),
    PhuongThuc VARCHAR(100) NOT NULL,
    Diem DECIMAL(4,2) NOT NULL,
    TrangThai VARCHAR(100) NOT NULL DEFAULT "Chờ duyệt",
    MaHSO VARCHAR(5),
    MaAdmin VARCHAR(4),
    FOREIGN KEY(MaNganh) REFERENCES Nganh(MaNganh),
    FOREIGN KEY(MaHSO) REFERENCES HSO_XETTUYEN(MaHSO),
    FOREIGN KEY(MaAdmin) REFERENCES QuanTri(MaAdmin)
);
```

## Quy trình tuyển sinh

```
┌─────────────────────────────────────────────────────────────┐
│                  TUYỂN SINH WORKFLOW                         │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  1. Thí sinh đăng ký                                        │
│     POST /api/auth/register-candidate                        │
│     → Tạo TK_XETTUYEN                                       │
│                                                              │
│  2. Thí sinh đăng nhập                                      │
│     POST /api/auth/login (role=candidate)                    │
│     → Nhận JWT token                                         │
│                                                              │
│  3. Thí sinh nộp hồ sơ                                      │
│     POST /api/tuyen-sinh/submit-profile                      │
│     → Tạo HSO_XETTUYEN (CCCD, SDT, HoTen)                   │
│                                                              │
│  4. Thí sinh nộp đơn xét tuyển                              │
│     POST /api/tuyen-sinh/submit-application                  │
│     → Tạo PT_XETTUYEN (TrangThai: "Chờ duyệt")              │
│                                                              │
│  5. Admin duyệt đơn                                          │
│     POST /api/tuyen-sinh/approve/<ma_ptxt>                   │
│     → TrangThai: "Đậu" + Auto tạo SinhVien                  │
│                                                              │
│  6. Admin từ chối                                            │
│     POST /api/tuyen-sinh/reject/<ma_ptxt>                   │
│     → TrangThai: "Rớt"                                       │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## Trạng thái phiếu

| Trạng thái | Mô tả |
|------------|-------|
| Chờ duyệt | Đơn mới nộp, chờ admin xử lý |
| Đậu | Admin duyệt → Auto tạo SinhVien |
| Rớt | Admin từ chối |

## API Endpoints

### Thí sinh

| Method | Endpoint | Mô tả | Auth |
|--------|----------|--------|------|
| POST | `/api/tuyen-sinh/submit-profile` | Nộp hồ sơ | Candidate |
| POST | `/api/tuyen-sinh/submit-application` | Nộp đơn | Candidate |
| GET | `/api/tuyen-sinh/status` | Trạng thái | Candidate |

### Admin

| Method | Endpoint | Mô tả | Auth |
|--------|----------|--------|------|
| GET | `/api/tuyen-sinh/pending` | DS chờ duyệt | Admin |
| GET | `/api/tuyen-sinh/all` | Tất cả phiếu | Admin |
| POST | `/api/tuyen-sinh/approve/<ma_ptxt>` | Duyệt đậu | Admin |
| POST | `/api/tuyen-sinh/reject/<ma_ptxt>` | Từ chối | Admin |
| POST | `/api/tuyen-sinh/approve-all` | Duyệt tất cả | Admin |

## Business Rules

### TK_XETTUYEN

- Email: Unique, đuôi `@gmail.com`
- MatKhau: Min 6 ký tự

### HSO_XETTUYEN

- CCCD: Unique, đúng 10 số
- SDT: Unique, đúng 10 số

### PT_XETTUYEN

- Diem: 0-30
- TrangThai: Chờ duyệt / Đậu / Rớt

## Dependencies

- Phụ thuộc: Nganh, QuanTri, TK_XETTUYEN
- Tạo: SinhVien (khi duyệt đậu)

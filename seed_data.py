"""
Seed Data Script - Populate QLSVSDH with sample data
Usage: python seed_data.py
"""
from werkzeug.security import generate_password_hash
import mysql.connector
from config import Config


def get_db_connection():
    return mysql.connector.connect(
        host=Config.MYSQL_HOST,
        port=Config.MYSQL_PORT,
        user=Config.MYSQL_USER,
        password=Config.MYSQL_PASSWORD,
        database=Config.MYSQL_DATABASE,
        charset="utf8mb4"
    )


def seed_all():
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        print("Seeding database...")

        seed_khoa(cursor)
        conn.commit()

        seed_nganh(cursor)
        conn.commit()

        seed_lop(cursor)
        conn.commit()

        seed_admins(cursor)
        conn.commit()

        seed_sinh_vien(cursor)
        conn.commit()

        seed_kq_hoc_tap(cursor)
        conn.commit()

        seed_thong_bao(cursor)
        conn.commit()

        print("\n✅ Seeding complete!")
        print_credentials()

    except Exception as e:
        conn.rollback()
        print(f"❌ Error: {e}")
        raise
    finally:
        cursor.close()
        conn.close()


def seed_khoa(cursor):
    print("  Seeding khoa...")
    for ma, ten in [
        ("CN", "Khoa Cong nghe thong tin"),
        ("KT", "Khoa Kinh te"),
        ("LQ", "Khoa Luat"),
    ]:
        cursor.execute(
            "INSERT IGNORE INTO khoa (ma_khoa, ten_khoa) VALUES (%s, %s)",
            (ma, ten)
        )
    print(f"    ✓ 3 departments seeded")


def seed_nganh(cursor):
    print("  Seeding nganh...")
    for ma, ten, mk in [
        ("CN01", "Khoa hoc may tinh", "CN"),
        ("CN02", "Cong nghe phan mem", "CN"),
        ("KT01", "Tai chinh Ngan hang", "KT"),
        ("LQ01", "Luat kinh te", "LQ"),
    ]:
        cursor.execute(
            "INSERT IGNORE INTO nganh (ma_nganh, ten_nganh, ma_khoa) VALUES (%s, %s, %s)",
            (ma, ten, mk)
        )
    print(f"    ✓ 4 majors seeded")


def seed_lop(cursor):
    print("  Seeding lop...")
    classes = [
        # Khoa CNTT - Khoa hoc may tinh
        ("D21CN01", "CNTT-K21", "CN01", "2021"),
        ("D22CN01", "CNTT-K22", "CN01", "2022"),
        ("D23CN01", "CNTT-K23", "CN01", "2023"),
        # Khoa CNTT - Cong nghe phan mem
        ("D21CN02", "CNPM-K21", "CN02", "2021"),
        ("D22CN02", "CNPM-K22", "CN02", "2022"),
        ("D23CN02", "CNPM-K23", "CN02", "2023"),
        # Khoa Kinh te - Tai chinh Ngan hang
        ("D21KT01", "TCNH-K21", "KT01", "2021"),
        ("D22KT01", "TCNH-K22", "KT01", "2022"),
        ("D23KT01", "TCNH-K23", "KT01", "2023"),
        # Khoa Luat - Luat kinh te
        ("D21LQ01", "LKT-K21", "LQ01", "2021"),
        ("D22LQ01", "LKT-K22", "LQ01", "2022"),
        ("D23LQ01", "LKT-K23", "LQ01", "2023"),
    ]
    for ma, ten, mn, kh in classes:
        cursor.execute(
            "INSERT IGNORE INTO lop (ma_lop, ten_lop, ma_nganh, khoa_hoc) VALUES (%s, %s, %s, %s)",
            (ma, ten, mn, kh)
        )
    print(f"    ✓ {len(classes)} classes seeded")


def seed_mon_hoc(cursor):
    print("  Seeding mon_hoc...")
    courses = [
        ("INT10001", "Nhap mon lap trinh", 3),
        ("INT10002", "Cau truc du lieu", 4),
        ("INT10003", "Co so du lieu", 3),
        ("INT10004", "Mang may tinh", 3),
        ("INT10005", "Tri tue nhan tao", 3),
        ("INT10006", "He dieu hanh", 3),
        ("INT10007", "Phat trien phan mem", 4),
        ("INT10008", "An toan thong tin", 3),
        ("MATH1001", "Toan cao cap", 4),
        ("MATH1002", "Xac suat thong ke", 3),
    ]
    for ma, ten, tc in courses:
        cursor.execute(
            "INSERT IGNORE INTO mon_hoc (ma_mh, ten_mh, so_tin_chi) VALUES (%s, %s, %s)",
            (ma, ten, tc)
        )
    print(f"    ✓ {len(courses)} courses seeded")


def seed_admins(cursor):
    print("  Seeding quan_tri (admins)...")
    admins = [
        ("QT001", "Administrator", "admin@qlsvsdh.com", "admin123"),
        ("QT002", "Nguyen Van Khoa", "khoa_cntt@qlsvsdh.com", "admin456"),
        ("QT003", "Tran Thi Mai", "mai_kinhte@qlsvsdh.com", "admin789"),
    ]
    for ma, ho_ten, email, pw in admins:
        ph = generate_password_hash(pw)
        cursor.execute(
            """INSERT IGNORE INTO quan_tri (ma_qt, ho_ten, email, password_hash)
               VALUES (%s, %s, %s, %s)""",
            (ma, ho_ten, email, ph)
        )
    print(f"    ✓ {len(admins)} admins seeded")


def seed_sinh_vien(cursor):
    print("  Seeding sinh_vien (students)...")
    students = [
        # CNTT-K21 (D21CN01) - 5 students
        ("B21DCCN001", "Nguyen Minh Anh", "anh.nm@svl.edu.vn", "B21DCCN001", "D21CN01", "0123456781", "001234567890"),
        ("B21DCCN002", "Le Hoang Nam", "nam.lh@svl.edu.vn", "B21DCCN002", "D21CN01", "0123456782", "001234567891"),
        ("B21DCCN003", "Pham Thu Ha", "ha.pt@svl.edu.vn", "B21DCCN003", "D21CN01", "0123456783", "001234567892"),
        ("B21DCCN004", "Hoang Duc Minh", "minh.hd@svl.edu.vn", "B21DCCN004", "D21CN01", "0123456784", "001234567893"),
        ("B21DCCN005", "Tran Lan Phuong", "phuong.tl@svl.edu.vn", "B21DCCN005", "D21CN01", "0123456785", "001234567894"),
        # CNPM-K21 (D21CN02) - 4 students
        ("B21DCCP001", "Vu Quang Huy", "huy.vq@svl.edu.vn", "B21DCCP001", "D21CN02", "0123456786", "001234567895"),
        ("B21DCCP002", "Dang Minh Thao", "thao.dm@svl.edu.vn", "B21DCCP002", "D21CN02", "0123456787", "001234567896"),
        ("B21DCCP003", "Bui Thanh Son", "son.bt@svl.edu.vn", "B21DCCP003", "D21CN02", "0123456788", "001234567897"),
        ("B21DCCP004", "Phan Thi Thanh Van", "van.ptt@svl.edu.vn", "B21DCCP004", "D21CN02", "0123456789", "001234567898"),
        # TCNH-K21 (D21KT01) - 4 students
        ("B21DKT001", "Ly Thi Mai Linh", "linh.lt@svl.edu.vn", "B21DKT001", "D21KT01", "0123456790", "001234567899"),
        ("B21DKT002", "Ngo Dinh Phong", "phong.nd@svl.edu.vn", "B21DKT002", "D21KT01", "0123456791", "001234567800"),
        ("B21DKT003", "Chu Thi Bich Ngoc", "ngoc.ctb@svl.edu.vn", "B21DKT003", "D21KT01", "0123456792", "001234567801"),
        ("B21DKT004", "Do Quang Vinh", "vinh.dq@svl.edu.vn", "B21DKT004", "D21KT01", "0123456793", "001234567802"),
        # LKT-K21 (D21LQ01) - 4 students
        ("B21DLQ001", "Trinh Minh Quan", "quan.tm@svl.edu.vn", "B21DLQ001", "D21LQ01", "0123456794", "001234567803"),
        ("B21DLQ002", "Dinh Thu Huong", "huong.dt@svl.edu.vn", "B21DLQ002", "D21LQ01", "0123456795", "001234567804"),
        ("B21DLQ003", "Cao Van Tien", "tien.cv@svl.edu.vn", "B21DLQ003", "D21LQ01", "0123456796", "001234567805"),
        ("B21DLQ004", "Nguyen Thi Thu Hien", "hien.ntt@svl.edu.vn", "B21DLQ004", "D21LQ01", "0123456797", "001234567806"),
        # CNTT-K22 (D22CN01) - 5 students
        ("B22DCCN001", "Pham Van Long", "long.pv@svl.edu.vn", "B22DCCN001", "D22CN01", "0123456798", "001234567807"),
        ("B22DCCN002", "Tran Thi Mai Anh", "anh.ttm@svl.edu.vn", "B22DCCN002", "D22CN01", "0123456799", "001234567808"),
        ("B22DCCN003", "Hoang Van Tuan", "tuan.hv@svl.edu.vn", "B22DCCN003", "D22CN01", "0123456800", "001234567809"),
        ("B22DCCN004", "La Thi Lan Huong", "huong.ltl@svl.edu.vn", "B22DCCN004", "D22CN01", "0123456801", "001234567810"),
        ("B22DCCN005", "Nguyen Van Hoang", "hoang.nv@svl.edu.vn", "B22DCCN005", "D22CN01", "0123456802", "001234567811"),
        # CNPM-K22 (D22CN02) - 4 students
        ("B22DCCP001", "Vu Thi Phuong Thao", "pthao.vt@svl.edu.vn", "B22DCCP001", "D22CN02", "0123456803", "001234567812"),
        ("B22DCCP002", "Tran Quang Nam", "nam.tq@svl.edu.vn", "B22DCCP002", "D22CN02", "0123456804", "001234567813"),
        ("B22DCCP003", "Le Thi Thu Ha", "ha.lth@svl.edu.vn", "B22DCCP003", "D22CN02", "0123456805", "001234567814"),
        ("B22DCCP004", "Phan Tien Dat", "dat.pt@svl.edu.vn", "B22DCCP004", "D22CN02", "0123456806", "001234567815"),
        # TCNH-K22 (D22KT01) - 4 students
        ("B22DKT001", "Pham Ngoc Lan", "lan.pn@svl.edu.vn", "B22DKT001", "D22KT01", "0123456807", "001234567816"),
        ("B22DKT002", "Trinh Van Tien", "tien.tv@svl.edu.vn", "B22DKT002", "D22KT01", "0123456808", "001234567817"),
        ("B22DKT003", "Nguyen Thi Bich Thao", "thao.ntbt@svl.edu.vn", "B22DKT003", "D22KT01", "0123456809", "001234567818"),
        ("B22DKT004", "Hoang Thanh Huan", "huan.ht@svl.edu.vn", "B22DKT004", "D22KT01", "0123456810", "001234567819"),
        # LKT-K22 (D22LQ01) - 4 students
        ("B22DLQ001", "Vu Van Thang", "thang.vv@svl.edu.vn", "B22DLQ001", "D22LQ01", "0123456811", "001234567820"),
        ("B22DLQ002", "Tran Thi Thu Thuy", "thuy.ttt@svl.edu.vn", "B22DLQ002", "D22LQ01", "0123456812", "001234567821"),
        ("B22DLQ003", "Ngo Dinh Hieu", "hieu.nd@svl.edu.vn", "B22DLQ003", "D22LQ01", "0123456813", "001234567822"),
        ("B22DLQ004", "Le Thi Thanh Truc", "truc.ltt@svl.edu.vn", "B22DLQ004", "D22LQ01", "0123456814", "001234567823"),
        # CNTT-K23 (D23CN01) - 5 students
        ("B23DCCN001", "Nguyen Huu Khoi", "khoi.nh@svl.edu.vn", "B23DCCN001", "D23CN01", "0123456815", "001234567824"),
        ("B23DCCN002", "Tran Ngoc Linh", "linh.tn@svl.edu.vn", "B23DCCN002", "D23CN01", "0123456816", "001234567825"),
        ("B23DCCN003", "Pham Quoc Viet", "viet.pq@svl.edu.vn", "B23DCCN003", "D23CN01", "0123456817", "001234567826"),
        ("B23DCCN004", "Ly Quynh Chi", "chi.lq@svl.edu.vn", "B23DCCN004", "D23CN01", "0123456818", "001234567827"),
        ("B23DCCN005", "Hoang Van Duc", "duc.hv@svl.edu.vn", "B23DCCN005", "D23CN01", "0123456819", "001234567828"),
        # CNPM-K23 (D23CN02) - 4 students
        ("B23DCCP001", "Le Thanh Mai", "mai.lt@svl.edu.vn", "B23DCCP001", "D23CN02", "0123456820", "001234567829"),
        ("B23DCCP002", "Vu Van Phuc", "phuc.vv@svl.edu.vn", "B23DCCP002", "D23CN02", "0123456821", "001234567830"),
        ("B23DCCP003", "Tran Van Sang", "sang.tv@svl.edu.vn", "B23DCCP003", "D23CN02", "0123456822", "001234567831"),
        ("B23DCCP004", "Nguyen Thi Thanh Hien", "hien.ntth@svl.edu.vn", "B23DCCP004", "D23CN02", "0123456823", "001234567832"),
        # TCNH-K23 (D23KT01) - 4 students
        ("B23DKT001", "Nguyen Thi Ngoc Anh", "anh.ntn@svl.edu.vn", "B23DKT001", "D23KT01", "0123456824", "001234567833"),
        ("B23DKT002", "Phan Van Dung", "dung.pv@svl.edu.vn", "B23DKT002", "D23KT01", "0123456825", "001234567834"),
        ("B23DKT003", "Tran Thi Hoai Thuong", "thuong.tth@svl.edu.vn", "B23DKT003", "D23KT01", "0123456826", "001234567835"),
        ("B23DKT004", "Do Van Manh", "manh.dv@svl.edu.vn", "B23DKT004", "D23KT01", "0123456827", "001234567836"),
        # LKT-K23 (D23LQ01) - 4 students
        ("B23DLQ001", "Pham Van Thanh", "thanh.pv@svl.edu.vn", "B23DLQ001", "D23LQ01", "0123456828", "001234567837"),
        ("B23DLQ002", "Nguyen Thi Hong Nhung", "nhung.nth@svl.edu.vn", "B23DLQ002", "D23LQ01", "0123456829", "001234567838"),
        ("B23DLQ003", "Tran Van Hao", "hao.tv@svl.edu.vn", "B23DLQ003", "D23LQ01", "0123456830", "001234567839"),
        ("B23DLQ004", "Phan Thi Xuan Mai", "mai.ptx@svl.edu.vn", "B23DLQ004", "D23LQ01", "0123456831", "001234567840"),
    ]
    for ma_sv, ho_ten, email, pw, ma_lop, sdt, cccd in students:
        ph = generate_password_hash(pw)
        cursor.execute(
            """INSERT IGNORE INTO sinh_vien
               (ma_sv, ho_ten, email, password_hash, ma_lop, so_dien_thoai, cccd, gpa)
               VALUES (%s, %s, %s, %s, %s, %s, %s, 0.0)""",
            (ma_sv, ho_ten, email, ph, ma_lop, sdt, cccd)
        )
    print(f"    ✓ {len(students)} students seeded")


def seed_kq_hoc_tap(cursor):
    print("  Seeding kq_hoc_tap (grades)...")

    cursor.execute("SELECT ma_sv FROM sinh_vien")
    ma_svs = [r[0] for r in cursor.fetchall()]
    cursor.execute("SELECT ma_mh FROM mon_hoc")
    ma_mhs = [r[0] for r in cursor.fetchall()]

    if not ma_mhs:
        print("    ⚠ mon_hoc table empty — skipping grade seeding")
        return

    cnnn = [s for s in ma_svs if s.startswith("B21DCCN") or s.startswith("B22DCCN") or s.startswith("B23DCCN")]
    cnpm = [s for s in ma_svs if s.startswith("B21DCCP") or s.startswith("B22DCCP") or s.startswith("B23DCCP")]
    kt   = [s for s in ma_svs if s.startswith("B21DKT") or s.startswith("B22DKT") or s.startswith("B23DKT")]
    lq   = [s for s in ma_svs if s.startswith("B21DLQ") or s.startswith("B22DLQ") or s.startswith("B23DLQ")]

    all_mh = ma_mhs
    basic_mh = [m for m in ma_mhs if m in ("INT10001", "MATH1001", "MATH1002")]

    grades = []
    for sv in cnnn:
        for i, mh in enumerate(all_mh):
            d = round(6.0 + i * 0.3 + (hash(sv + mh) % 20) / 10.0, 2)
            grades.append((sv, mh, min(10.0, max(4.0, d))))

    for sv in cnpm:
        for i, mh in enumerate(all_mh):
            d = round(5.5 + i * 0.25 + (hash(sv + mh) % 18) / 10.0, 2)
            grades.append((sv, mh, min(10.0, max(4.0, d))))

    math_mh = [m for m in ma_mhs if m.startswith("MATH")]
    int_mh  = [m for m in ma_mhs if m in ("INT10001", "INT10003", "INT10004")]
    for sv in kt:
        for i, mh in enumerate(math_mh + int_mh):
            d = round(6.5 + i * 0.2 + (hash(sv + mh) % 15) / 10.0, 2)
            grades.append((sv, mh, min(10.0, max(4.0, d))))

    for sv in lq:
        for i, mh in enumerate(basic_mh):
            d = round(7.0 + i * 0.1 + (hash(sv + mh) % 12) / 10.0, 2)
            grades.append((sv, mh, min(10.0, max(4.0, d))))

    for ma_sv, ma_mh, diem in grades:
        cursor.execute(
            "INSERT IGNORE INTO kq_hoc_tap (ma_sv, ma_mh, diem) VALUES (%s, %s, %s)",
            (ma_sv, ma_mh, diem)
        )
    print(f"    ✓ {len(grades)} grade records seeded")


def seed_thong_bao(cursor):
    print("  Seeding thong_bao...")
    cursor.execute("SELECT ma_qt FROM quan_tri LIMIT 1")
    ma_admin = cursor.fetchone()[0]

    notifications = [
        ("TB00000001", "Thong bao lich thi cuoi ky",
         f"Lich thi cuoi ky tu 15/01 den 30/01. SV chu y theo doi.", ma_admin),
        ("TB00000002", "Dang ky hoc phan HK2",
         f"Dang ky hoc phan HK2 bat dau 10/12. Dang ky qua he thong.", ma_admin),
        ("TB00000003", "Nghi le Giang sinh",
         "Truong nghi le Giang sinh tu 24/12 den 26/12.", ma_admin),
        ("TB00000004", "Tuyen sinh thuc tap",
         "Cac cong ty tuyen SV thuc tap. Chi tiet tai phong CTSV.", ma_admin),
    ]
    for ma_tb, tieu_de, noi_dung, ma_qt in notifications:
        cursor.execute(
            """INSERT IGNORE INTO thong_bao (ma_tb, tieu_de, noi_dung, nguoi_tao)
               VALUES (%s, %s, %s, %s)""",
            (ma_tb, tieu_de, noi_dung, ma_qt)
        )
    print(f"    ✓ {len(notifications)} notifications seeded")


def print_credentials():
    print("\n" + "=" * 55)
    print("  DEFAULT CREDENTIALS")
    print("=" * 55)
    print("\n  Admin accounts:")
    print("    admin@qlsvsdh.com / admin123  (QT001 - Administrator)")
    print("    khoa_cntt@qlsvsdh.com / admin456 (QT002 - Nguyen Van Khoa)")
    print("    mai_kinhte@qlsvsdh.com / admin789 (QT003 - Tran Thi Mai)")
    print("\n  Student accounts:")
    print("    B21DCCN001 / B21DCCN001")
    print("    B21DCCP001 / B21DCCP001")
    print("    B21DKT001 / B21DKT001")
    print("    B21DLQ001 / B21DLQ001")
    print("  (All other students: username = password = ma_sv)")
    print("=" * 55)


if __name__ == "__main__":
    seed_all()

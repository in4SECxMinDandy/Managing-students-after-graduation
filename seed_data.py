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

        seed_mon_hoc(cursor)
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
    for ma, ten, mn in [
        ("D21CN01", "CNTT-K21", "CN01"),
        ("D21CN02", "CNPM-K21", "CN02"),
        ("D21KT01", "TCNH-K21", "KT01"),
        ("D21LQ01", "LKT-K21", "LQ01"),
    ]:
        cursor.execute(
            "INSERT IGNORE INTO lop (ma_lop, ten_lop, ma_nganh, khoa_hoc) VALUES (%s, %s, %s, %s)",
            (ma, ten, mn, "2021")
        )
    print(f"    ✓ 4 classes seeded")


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
        # CNTT class
        ("B21DCCN001", "Nguyen Minh Anh", "anh.nm@svl.edu.vn", "B21DCCN001", "D21CN01", "0123456781", "001234567890"),
        ("B21DCCN002", "Le Hoang Nam", "nam.lh@svl.edu.vn", "B21DCCN002", "D21CN01", "0123456782", "001234567891"),
        ("B21DCCN003", "Pham Thu Ha", "ha.pt@svl.edu.vn", "B21DCCN003", "D21CN01", "0123456783", "001234567892"),
        ("B21DCCN004", "Hoang Duc Minh", "minh.hd@svl.edu.vn", "B21DCCN004", "D21CN01", "0123456784", "001234567893"),
        ("B21DCCN005", "Tran Lan Phuong", "phuong.tl@svl.edu.vn", "B21DCCN005", "D21CN01", "0123456785", "001234567894"),
        # CNPM class
        ("B21DCCP001", "Vu Quang Huy", "huy.vq@svl.edu.vn", "B21DCCP001", "D21CN02", "0123456786", "001234567895"),
        ("B21DCCP002", "Dang Minh Thao", "thao.dm@svl.edu.vn", "B21DCCP002", "D21CN02", "0123456787", "001234567896"),
        ("B21DCCP003", "Bui Thanh Son", "son.bt@svl.edu.vn", "B21DCCP003", "D21CN02", "0123456788", "001234567897"),
        # KinhTe class
        ("B21DKT001", "Ly Thi Mai Linh", "linh.lt@svl.edu.vn", "B21DKT001", "D21KT01", "0123456789", "001234567898"),
        ("B21DKT002", "Ngo Dinh Phong", "phong.nd@svl.edu.vn", "B21DKT002", "D21KT01", "0123456790", "001234567899"),
        ("B21DKT003", "Chu Thi Bich Ngoc", "ngoc.ctb@svl.edu.vn", "B21DKT003", "D21KT01", "0123456791", "001234567800"),
        # Luat class
        ("B21DLQ001", "Trinh Minh Quan", "quan.tm@svl.edu.vn", "B21DLQ001", "D21LQ01", "0123456792", "001234567801"),
        ("B21DLQ002", "Dinh Thu Huong", "huong.dt@svl.edu.vn", "B21DLQ002", "D21LQ01", "0123456793", "001234567802"),
        ("B21DLQ003", "Cao Van Tien", "tien.cv@svl.edu.vn", "B21DLQ003", "D21LQ01", "0123456794", "001234567803"),
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

    cnnn = [s for s in ma_svs if s.startswith("B21DCCN")]
    cnpm = [s for s in ma_svs if s.startswith("B21DCCP")]
    kt   = [s for s in ma_svs if s.startswith("B21DKT")]
    lq   = [s for s in ma_svs if s.startswith("B21DLQ")]

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

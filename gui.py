"""
QLSVSDH GUI - Python Tkinter GUI
Chạy: python gui.py

Điều khiển: Ctrl+C trong terminal để thoát
"""
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import requests
import json
from typing import Optional, Dict, Any

# ========== API Configuration ==========
API_BASE_URL = "http://localhost:5000/api"


class APIClient:
    """HTTP client gọi Flask API"""

    def __init__(self):
        self.token: Optional[str] = None
        self.user: Optional[Dict] = None
        self.role: Optional[str] = None

    def set_auth(self, token: str, user: Dict, role: str):
        self.token = token
        self.user = user
        self.role = role

    def clear_auth(self):
        self.token = None
        self.user = None
        self.role = None

    def get_headers(self) -> Dict:
        if self.token:
            return {"Authorization": f"Bearer {self.token}", "Content-Type": "application/json"}
        return {"Content-Type": "application/json"}

    def get(self, endpoint: str) -> Dict:
        try:
            response = requests.get(f"{API_BASE_URL}{endpoint}", headers=self.get_headers(), timeout=10)
            return response.json()
        except requests.exceptions.ConnectionError:
            return {"error": "Không thể kết nối server. Vui lòng chạy: python run.py"}
        except Exception as e:
            return {"error": str(e)}

    def post(self, endpoint: str, data: Dict = None) -> Dict:
        try:
            response = requests.post(f"{API_BASE_URL}{endpoint}",
                                    json=data or {},
                                    headers=self.get_headers(),
                                    timeout=10)
            return response.json()
        except requests.exceptions.ConnectionError:
            return {"error": "Không thể kết nối server. Vui lòng chạy: python run.py"}
        except Exception as e:
            return {"error": str(e)}

    def put(self, endpoint: str, data: Dict) -> Dict:
        try:
            response = requests.put(f"{API_BASE_URL}{endpoint}",
                                   json=data,
                                   headers=self.get_headers(),
                                   timeout=10)
            return response.json()
        except Exception as e:
            return {"error": str(e)}

    def delete(self, endpoint: str) -> Dict:
        try:
            response = requests.delete(f"{API_BASE_URL}{endpoint}",
                                      headers=self.get_headers(),
                                      timeout=10)
            return response.json()
        except Exception as e:
            return {"error": str(e)}


api = APIClient()


# ========== Utility Functions ==========

def center_window(win, width=800, height=600):
    """Căn giữa cửa sổ"""
    win.update_idletasks()
    screen_width = win.winfo_screenwidth()
    screen_height = win.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    win.geometry(f"{width}x{height}+{x}+{y}")


def style_button(btn, bg="#1976D2", fg="white"):
    """Style button đẹp"""
    btn.configure(bg=bg, fg=fg, font=("Segoe UI", 10, "bold"),
                  relief="flat", padx=15, pady=8, cursor="hand2")


def style_entry(entry):
    """Style entry"""
    entry.configure(font=("Segoe UI", 10), relief="solid", bd=1)


# ========== Login Window ==========

class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("QLSVSDH - Đăng nhập")
        center_window(self.root, 400, 450)
        self.root.configure(bg="#f5f5f5")

        self.setup_ui()

    def setup_ui(self):
        # Title
        title_frame = tk.Frame(self.root, bg="#1565C0", height=100)
        title_frame.pack(fill="x")
        title_frame.pack_propagate(False)

        title_label = tk.Label(title_frame, text="QLSVSDH",
                              font=("Segoe UI", 24, "bold"),
                              bg="#1565C0", fg="white")
        title_label.pack(pady=25)

        subtitle = tk.Label(title_frame, text="Quản lý Sinh viên Đại học",
                           font=("Segoe UI", 10), bg="#1565C0", fg="#BBDEFB")
        subtitle.pack()

        # Login form
        form_frame = tk.Frame(self.root, bg="white", bd=2, relief="ridge")
        form_frame.pack(pady=30, padx=40, fill="both", expand=True)

        tk.Label(form_frame, text="ĐĂNG NHẬP HỆ THỐNG",
                font=("Segoe UI", 14, "bold"), bg="white",
                fg="#333").pack(pady=20)

        # Role selection
        tk.Label(form_frame, text="Vai trò:", font=("Segoe UI", 10),
                bg="white").pack(anchor="w", padx=50)

        self.role_var = tk.StringVar(value="admin")
        role_frame = tk.Frame(form_frame, bg="white")
        role_frame.pack(pady=5, padx=50, fill="x")

        roles = [("Admin", "admin"), ("Sinh viên", "student")]
        for text, value in roles:
            rb = tk.Radiobutton(role_frame, text=text, variable=self.role_var,
                               value=value, font=("Segoe UI", 10), bg="white",
                               command=self.on_role_change)
            rb.pack(side="left", padx=10)

        # Fields frame
        self.fields_frame = tk.Frame(form_frame, bg="white")
        self.fields_frame.pack(pady=10, padx=50, fill="x")

        self.username_label = tk.Label(self.fields_frame, text="Tên đăng nhập:",
                                      font=("Segoe UI", 10), bg="white")
        self.username_label.pack(anchor="w")
        self.username_entry = tk.Entry(self.fields_frame, font=("Segoe UI", 11),
                                       width=30)
        self.username_entry.pack(pady=5, ipady=5)

        self.password_label = tk.Label(self.fields_frame, text="Mật khẩu:",
                                      font=("Segoe UI", 10), bg="white")
        self.password_label.pack(anchor="w")
        self.password_entry = tk.Entry(self.fields_frame, font=("Segoe UI", 11),
                                      width=30, show="*")
        self.password_entry.pack(pady=5, ipady=5)

        # Login button
        self.login_btn = tk.Button(form_frame, text="ĐĂNG NHẬP",
                                   command=self.do_login,
                                   font=("Segoe UI", 11, "bold"),
                                   bg="#1976D2", fg="white",
                                   relief="flat", padx=30, pady=10,
                                   cursor="hand2")
        self.login_btn.pack(pady=20)

        self.login_btn.bind("<Enter>", lambda e: self.login_btn.configure(bg="#1565C0"))
        self.login_btn.bind("<Leave>", lambda e: self.login_btn.configure(bg="#1976D2"))

        # Enter key
        self.password_entry.bind("<Return>", lambda e: self.do_login())

    def on_role_change(self):
        """Thay đổi label theo role"""
        role = self.role_var.get()
        if role == "admin":
            self.username_label.config(text="Tên đăng nhập:")
            self.password_label.config(text="Mật khẩu:")
        elif role == "student":
            self.username_label.config(text="Mã sinh viên:")
            self.password_label.config(text="Mật khẩu:")

        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)

    def do_login(self):
        """Xử lý đăng nhập"""
        role = self.role_var.get()
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập đầy đủ thông tin")
            return

        # Build login data
        if role == "admin":
            data = {"role": "admin", "ten_dn": username, "mat_khau": password}
        elif role == "student":
            data = {"role": "student", "ma_sv": username, "mat_khau": password}
        else:
            messagebox.showerror("Lỗi", "Vai trò không hợp lệ")
            return

        self.login_btn.config(state="disabled", text="Đang đăng nhập...")

        result = api.post("/auth/login", data)

        self.login_btn.config(state="normal", text="ĐĂNG NHẬP")

        if "error" in result:
            messagebox.showerror("Lỗi", result.get("error", "Lỗi kết nối"))
            return

        if result.get("success"):
            api.set_auth(result["token"], result["user"], role)
            self.root.withdraw()
            self.open_dashboard()
        else:
            messagebox.showerror("Lỗi", result.get("message", "Đăng nhập thất bại"))

    def open_dashboard(self):
        """Mo dashboard theo role"""
        # Tao cua so moi, khong reuse root cua login
        dashboard_root = tk.Toplevel()
        dashboard_root.protocol("WM_DELETE_WINDOW", lambda: self._exit_app(dashboard_root))

        if api.role == "admin":
            AdminDashboard(dashboard_root)
        elif api.role == "student":
            StudentDashboard(dashboard_root)

    def _exit_app(self, win):
        """Dong tat ca cua so khi logout hoac tat dashboard"""
        win.destroy()
        self.root.destroy()   # dong ca login window
        # Ket thuc vong lap chinh
        if hasattr(self, '_mainloop_running'):
            self.root.quit()


# ========== Main Entry Point ==========

class BaseDashboard:
    def __init__(self, root, title: str):
        self.root = root
        self.root.title(f"QLSVSDH - {title}")
        center_window(self.root, 1200, 700)
        self.root.configure(bg="#f5f5f5")

        self.setup_ui()
        self.load_data()

    def setup_ui(self):
        """Override in subclass"""
        pass

    def load_data(self):
        """Override in subclass"""
        pass

    def create_nav_button(self, parent, text, command):
        """Tạo nav button"""
        btn = tk.Button(parent, text=text, command=command,
                       font=("Segoe UI", 10), bg="#424242", fg="white",
                       relief="flat", anchor="w", padx=20, pady=12,
                       cursor="hand2")
        btn.bind("<Enter>", lambda e: btn.configure(bg="#616161"))
        btn.bind("<Leave>", lambda e: btn.configure(bg="#424242"))
        return btn

    def logout(self):
        """Đăng xuất"""
        if messagebox.askyesno("Xác nhận", "Bạn có muốn đăng xuất?"):
            api.clear_auth()
            self.root.destroy()            # dong dashboard
            LoginWindow(tk.Tk())          # mo lai cua so dang nhap

    def show_error(self, msg):
        messagebox.showerror("Lỗi", msg)


# ========== Admin Dashboard ==========

class AdminDashboard(BaseDashboard):
    def __init__(self, root):
        self.current_view = None
        self.data_cache = {}
        super().__init__(root, "Quản trị viên")

    def setup_ui(self):
        # Top header
        header = tk.Frame(self.root, bg="#1565C0", height=60)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(header, text="QUẢN TRỊ HỆ THỐNG",
                font=("Segoe UI", 16, "bold"),
                bg="#1565C0", fg="white").pack(side="left", padx=20)

        user_label = tk.Label(header, text=f"Xin chào: {api.user.get('ho_ten', api.user.get('email', ''))}",
                            font=("Segoe UI", 10), bg="#1565C0", fg="#BBDEFB")
        user_label.pack(side="right", padx=20)

        tk.Button(header, text="Đăng xuất", command=self.logout,
                 bg="#D32F2F", fg="white", relief="flat",
                 cursor="hand2").pack(side="right", padx=10)

        # Main content
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill="both", expand=True)

        # Sidebar
        sidebar = tk.Frame(main_frame, bg="#212121", width=200)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        nav_items = [
            ("Trang chủ", self.show_home),
            ("Khoa", lambda: self.show_crud("Khoa", "/khoa/")),
            ("Ngành", lambda: self.show_crud("Ngành", "/nganh/")),
            ("Lớp", lambda: self.show_crud("Lớp", "/lop/")),
            ("Môn học", lambda: self.show_crud("Môn học", "/mon-hoc/")),
            ("Sinh viên", self.show_sinh_vien),
            ("Học tập", self.show_hoc_tap),
            ("Tốt nghiệp", self.show_tot_nghiep),
            ("Thông báo", self.show_thong_bao),
            ("Quản trị", self.show_quan_tri),
        ]

        tk.Label(sidebar, text="MENU", font=("Segoe UI", 10, "bold"),
                bg="#212121", fg="#9E9E9E").pack(pady=15, padx=10)

        for text, cmd in nav_items:
            self.create_nav_button(sidebar, text, cmd).pack(fill="x", padx=5, pady=2)

        # Content area
        self.content = tk.Frame(main_frame, bg="#f5f5f5")
        self.content.pack(side="right", fill="both", expand=True)

        self.show_home()

    def show_home(self):
        """Trang chủ admin"""
        self.clear_content()

        # Stats cards
        stats_frame = tk.Frame(self.content, bg="#f5f5f5")
        stats_frame.pack(pady=20, padx=20)

        stats = [
            ("Tổng sinh viên", "/sinh-vien/", "👥"),
            ("Khoa", "/khoa/", "🏛️"),
            ("Ngành", "/nganh/", "📚"),
        ]

        for title, endpoint, icon in stats:
            card = tk.Frame(stats_frame, bg="white", bd=2, relief="ridge", width=200, height=100)
            card.pack(side="left", padx=10, pady=10)
            card.pack_propagate(False)

            tk.Label(card, text=icon, font=("Segoe UI", 24),
                    bg="white").pack(pady=10)
            tk.Label(card, text=title, font=("Segoe UI", 10),
                    bg="white", fg="#666").pack()

    def show_crud(self, title: str, endpoint: str):
        """Generic CRUD view"""
        self.clear_content()

        header = tk.Frame(self.content, bg="white", height=50)
        header.pack(fill="x", padx=10, pady=(10, 0))
        header.pack_propagate(False)

        tk.Label(header, text=f"Quản lý {title}",
                font=("Segoe UI", 14, "bold"),
                bg="white").pack(side="left", padx=10, pady=10)

        tk.Button(header, text=f"+ Thêm {title}",
                command=lambda: self.add_item(title, endpoint),
                bg="#4CAF50", fg="white", relief="flat",
                cursor="hand2").pack(side="right", padx=10)

        # Table
        table_frame = tk.Frame(self.content, bg="white")
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)

        result = api.get(endpoint)
        if "error" in result:
            tk.Label(table_frame, text=result["error"],
                    fg="red").pack()
            return

        data = result.get("data", [])
        if not data:
            tk.Label(table_frame, text=f"Chưa có dữ liệu {title}",
                    font=("Segoe UI", 12), bg="white").pack(pady=50)
            return

        # Headers
        headers = list(data[0].keys())
        for i, h in enumerate(headers):
            tk.Label(table_frame, text=h, font=("Segoe UI", 10, "bold"),
                    bg="#1976D2", fg="white", relief="ridge",
                    width=15).grid(row=0, column=i, sticky="nsew", padx=1, pady=1)

        # Rows
        for row_idx, row in enumerate(data):
            for col_idx, key in enumerate(headers):
                val = str(row.get(key, ""))
                bg = "white" if row_idx % 2 == 0 else "#E3F2FD"
                tk.Label(table_frame, text=val[:30], font=("Segoe UI", 9),
                        bg=bg, relief="ridge", anchor="w",
                        width=15).grid(row=row_idx + 1, column=col_idx,
                                      sticky="nsew", padx=1, pady=1)

            # Action buttons
            btn_frame = tk.Frame(table_frame, bg=bg)
            btn_frame.grid(row=row_idx + 1, column=len(headers),
                         sticky="nsew", padx=1, pady=1)
            tk.Button(btn_frame, text="Sửa",
                     command=lambda r=row, e=endpoint: self.edit_item(title, e, r),
                     font=("Segoe UI", 8), bg="#FFC107", relief="flat",
                     cursor="hand2").pack(side="left", padx=2)
            tk.Button(btn_frame, text="Xóa",
                     command=lambda r=row, e=endpoint, k=headers[0]: self.delete_item(title, e, r.get(k)),
                     font=("Segoe UI", 8), bg="#D32F2F", fg="white",
                     relief="flat", cursor="hand2").pack(side="left", padx=2)

    def show_sinh_vien(self):
        """Quản lý sinh viên"""
        self.clear_content()

        header = tk.Frame(self.content, bg="white", height=50)
        header.pack(fill="x", padx=10, pady=(10, 0))
        header.pack_propagate(False)

        tk.Label(header, text="Quản lý Sinh viên",
                font=("Segoe UI", 14, "bold"),
                bg="white").pack(side="left", padx=10, pady=10)

        tk.Button(header, text="+ Thêm SV",
                 command=self.add_sinh_vien,
                 bg="#4CAF50", fg="white", relief="flat",
                 cursor="hand2").pack(side="right", padx=10)

        # Load lop data for edit forms
        self._sv_lop_options = []
        lop_result = api.get("/lop/")
        if lop_result.get("data"):
            self._sv_lop_options = [(r.get("MaLop", ""), r.get("TenLop", ""))
                                     for r in lop_result["data"]]

        # Table
        table_frame = tk.Frame(self.content, bg="white")
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)

        result = api.get("/sinh-vien/")
        if "error" in result:
            tk.Label(table_frame, text=result["error"], fg="red").pack()
            return

        data = result.get("data", [])
        if not data:
            tk.Label(table_frame, text="Chưa có sinh viên",
                    font=("Segoe UI", 12), bg="white").pack(pady=50)
            return

        # Headers: MaSV, HoTen, NgaySinh, Email, MaLop
        sv_headers = ["ma_sv", "ho_ten", "ngay_sinh", "email", "ma_lop"]
        col_widths = [12, 20, 12, 25, 10]
        for i, (h, w) in enumerate(zip(sv_headers, col_widths)):
            tk.Label(table_frame, text=h, font=("Segoe UI", 10, "bold"),
                    bg="#1976D2", fg="white", relief="ridge",
                    width=w).grid(row=0, column=i, sticky="nsew", padx=1, pady=1)

        for row_idx, row in enumerate(data):
            for col_idx, key in enumerate(sv_headers):
                val = str(row.get(key, ""))
                bg = "white" if row_idx % 2 == 0 else "#E3F2FD"
                tk.Label(table_frame, text=val[:30], font=("Segoe UI", 9),
                        bg=bg, relief="ridge", anchor="w",
                        width=col_widths[col_idx]).grid(
                    row=row_idx + 1, column=col_idx, sticky="nsew", padx=1, pady=1)
            # Action buttons
            btn_frame = tk.Frame(table_frame, bg=bg)
            btn_frame.grid(row=row_idx + 1, column=len(sv_headers),
                         sticky="nsew", padx=1, pady=1)
            tk.Button(btn_frame, text="Sửa",
                     command=lambda r=row: self.edit_sinh_vien(r),
                     font=("Segoe UI", 8), bg="#FFC107", relief="flat",
                     cursor="hand2").pack(side="left", padx=2)
            tk.Button(btn_frame, text="Xóa",
                     command=lambda r=row: self.delete_sinh_vien(r),
                     font=("Segoe UI", 8), bg="#D32F2F", fg="white",
                     relief="flat", cursor="hand2").pack(side="left", padx=2)

    def add_sinh_vien(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Thêm Sinh viên")
        center_window(dialog, 420, 380)
        dialog.configure(bg="white")

        tk.Label(dialog, text="Thêm Sinh viên mới", font=("Segoe UI", 12, "bold"),
                bg="white").pack(pady=10)

        fields = [
            ("Mã SV:", "ma_sv"), ("Họ tên:", "ho_ten"),
            ("Ngày sinh:", "ngay_sinh"), ("Email:", "email"),
            ("Mật khẩu:", "password_hash"), ("Mã Lớp:", "ma_lop"),
            ("SDT:", "so_dien_thoai"), ("CCCD:", "cccd"),
        ]
        entries = {}
        form_frame = tk.Frame(dialog, bg="white")
        form_frame.pack(fill="x", padx=20, pady=5)
        for label, key in fields:
            fr = tk.Frame(form_frame, bg="white")
            fr.pack(fill="x", pady=3)
            tk.Label(fr, text=label, width=14, bg="white", anchor="e").pack(side="left")
            show = "*" if key == "password_hash" else ""
            e = tk.Entry(fr, font=("Segoe UI", 10), show=show)
            e.pack(side="right", fill="x", expand=True)
            entries[key] = e

        def submit():
            data = {k: e.get().strip() for k, e in entries.items()}
            if not data.get("ma_sv") or not data.get("ho_ten"):
                messagebox.showerror("Lỗi", "Mã SV và Họ tên bắt buộc")
                return
            result = api.post("/sinh-vien/", data)
            if result.get("success"):
                messagebox.showinfo("Thành công", "Đã thêm sinh viên")
                dialog.destroy()
                self.show_sinh_vien()
            else:
                messagebox.showerror("Lỗi", result.get("message", result.get("error", "Lỗi")))

        tk.Button(dialog, text="Lưu", command=submit,
                 bg="#4CAF50", fg="white", relief="flat", cursor="hand2").pack(pady=10)

    def edit_sinh_vien(self, row):
        dialog = tk.Toplevel(self.root)
        dialog.title("Sửa Sinh viên")
        center_window(dialog, 420, 340)
        dialog.configure(bg="white")

        ma_sv = row.get("ma_sv", "")

        tk.Label(dialog, text=f"Sửa: {ma_sv}", font=("Segoe UI", 12, "bold"),
                bg="white").pack(pady=10)

        fields = [
            ("Mã SV:", "ma_sv", True), ("Họ tên:", "ho_ten", False),
            ("Email:", "email", False), ("SDT:", "so_dien_thoai", False),
            ("CCCD:", "cccd", False),
        ]
        entries = {}
        form_frame = tk.Frame(dialog, bg="white")
        form_frame.pack(fill="x", padx=20, pady=5)
        for label, key, readonly in fields:
            fr = tk.Frame(form_frame, bg="white")
            fr.pack(fill="x", pady=3)
            tk.Label(fr, text=label, width=14, bg="white", anchor="e").pack(side="left")
            e = tk.Entry(form_frame, font=("Segoe UI", 10))
            e.insert(0, str(row.get(key, "")))
            if readonly:
                e.configure(state="readonly")
            e.pack(fill="x")
            entries[key] = e

        def submit():
            data = {k: e.get().strip() for k, e in entries.items()}
            payload = {k: v for k, v in data.items() if k != "MaSV"}
            result = api.put(f"/sinh-vien/{ma_sv}", payload)
            if result.get("success"):
                messagebox.showinfo("Thành công", "Đã cập nhật")
                dialog.destroy()
                self.show_sinh_vien()
            else:
                messagebox.showerror("Lỗi", result.get("message", result.get("error", "Lỗi")))

        tk.Button(dialog, text="Lưu", command=submit,
                 bg="#1976D2", fg="white", relief="flat", cursor="hand2").pack(pady=10)

    def delete_sinh_vien(self, row):
        ma_sv = row.get("ma_sv", "")
        if messagebox.askyesno("Xác nhận", f"Xóa sinh viên {ma_sv}?"):
            result = api.delete(f"/sinh-vien/{ma_sv}")
            if result.get("success"):
                messagebox.showinfo("Thành công", "Đã xóa sinh viên")
                self.show_sinh_vien()
            else:
                messagebox.showerror("Lỗi", result.get("message", "Lỗi"))

    def show_hoc_tap(self):
        """Quản lý học tập"""
        self.clear_content()

        header = tk.Frame(self.content, bg="white", height=50)
        header.pack(fill="x", padx=10, pady=(10, 0))

        tk.Label(header, text="Quản lý Điểm",
                font=("Segoe UI", 14, "bold"),
                bg="white").pack(side="left", padx=10, pady=10)

        tk.Button(header, text="Nhập điểm",
                 command=self.nhap_diem_admin,
                 bg="#4CAF50", fg="white", relief="flat",
                 cursor="hand2").pack(side="right", padx=10)

        # MaSV input
        input_frame = tk.Frame(self.content, bg="white")
        input_frame.pack(fill="x", padx=10, pady=10)

        tk.Label(input_frame, text="Mã SV:", font=("Segoe UI", 10)).pack(side="left", padx=5)
        self.ma_sv_entry = tk.Entry(input_frame, font=("Segoe UI", 10), width=15)
        self.ma_sv_entry.pack(side="left", padx=5)
        tk.Button(input_frame, text="Xem điểm",
                 command=self.xem_diem,
                 bg="#1976D2", fg="white", relief="flat",
                 cursor="hand2").pack(side="left", padx=5)
        tk.Button(input_frame, text="Tính GPA",
                 command=self.tinh_gpa,
                 bg="#FF9800", fg="white", relief="flat",
                 cursor="hand2").pack(side="left", padx=5)

        self.diem_result = tk.Frame(self.content, bg="white")
        self.diem_result.pack(fill="both", expand=True, padx=10, pady=10)

    def xem_diem(self):
        """Xem điểm sinh viên"""
        for w in self.diem_result.winfo_children():
            w.destroy()

        ma_sv = self.ma_sv_entry.get().strip()
        if not ma_sv:
            tk.Label(self.diem_result, text="Nhập mã SV",
                    font=("Segoe UI", 10), bg="white").pack()
            return

        result = api.get(f"/hoc-tap/diem/{ma_sv}")
        if "error" in result:
            tk.Label(self.diem_result, text=result["error"],
                    fg="red", bg="white").pack()
            return

        data = result.get("data", [])
        if not data:
            tk.Label(self.diem_result, text="Chưa có điểm",
                    font=("Segoe UI", 10), bg="white").pack()
            return

        headers = ["Mã MH", "Tên môn", "Số TC", "Điểm"]
        for i, h in enumerate(headers):
            tk.Label(self.diem_result, text=h, font=("Segoe UI", 9, "bold"),
                    bg="#1976D2", fg="white", relief="ridge",
                    width=12).grid(row=0, column=i, sticky="nsew", padx=1, pady=1)

        for row_idx, d in enumerate(data):
            values = [d.get("ma_mh", ""), d.get("ten_mh", ""),
                     str(d.get("so_tin_chi", "")), str(d.get("diem", ""))]
            for col_idx, val in enumerate(values):
                bg = "white" if row_idx % 2 == 0 else "#E3F2FD"
                tk.Label(self.diem_result, text=str(val)[:20], font=("Segoe UI", 9),
                        bg=bg, relief="ridge", anchor="w",
                        width=12).grid(row=row_idx + 1, column=col_idx,
                                      sticky="nsew", padx=1, pady=1)

    def tinh_gpa(self):
        """Tính GPA"""
        ma_sv = self.ma_sv_entry.get().strip()
        if not ma_sv:
            return
        result = api.get(f"/hoc-tap/gpa/{ma_sv}")
        if result.get("success"):
            data = result["data"]
            messagebox.showinfo("GPA",
                f"Mã SV: {data['ma_sv']}\n"
                f"GPA thang 10: {data['gpa_thang_10']}\n"
                f"GPA thang 4: {data['gpa_thang_4']}\n"
                f"Tổng tín chỉ: {data['tong_tin_chi']}\n"
                f"Số môn: {data['so_mon']}")
        else:
            messagebox.showerror("Lỗi", result.get("message", "Lỗi"))

    def nhap_diem_admin(self):
        """Nhập điểm dialog"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Nhập điểm")
        center_window(dialog, 350, 250)
        dialog.configure(bg="white")

        tk.Label(dialog, text="Nhập điểm", font=("Segoe UI", 12, "bold"),
                bg="white").pack(pady=10)

        fields = [("Mã SV:", "ma_sv"), ("Mã MH:", "ma_mh"), ("Điểm:", "diem")]
        entries = {}
        for label, key in fields:
            fr = tk.Frame(dialog, bg="white")
            fr.pack(fill="x", padx=20, pady=5)
            tk.Label(fr, text=label, width=10, bg="white").pack(side="left")
            e = tk.Entry(fr, font=("Segoe UI", 10))
            e.pack(side="right", fill="x", expand=True)
            entries[key] = e

        def submit():
            data = {k: e.get().strip() for k, e in entries.items()}
            try:
                data["diem"] = float(data["diem"])
            except:
                messagebox.showerror("Lỗi", "Điểm phải là số")
                return

            result = api.post("/hoc-tap/diem", data)
            if result.get("success"):
                messagebox.showinfo("Thành công", "Đã nhập điểm")
                dialog.destroy()
            else:
                messagebox.showerror("Lỗi", result.get("message", "Lỗi"))

        tk.Button(dialog, text="Lưu", command=submit,
                 bg="#4CAF50", fg="white", relief="flat",
                 cursor="hand2").pack(pady=15)

    def show_tot_nghiep(self):
        """Quản lý tốt nghiệp"""
        self.clear_content()

        header = tk.Frame(self.content, bg="white", height=50)
        header.pack(fill="x", padx=10, pady=(10, 0))

        tk.Label(header, text="Xét Tốt nghiệp",
                font=("Segoe UI", 14, "bold"),
                bg="white").pack(side="left", padx=10, pady=10)

        input_frame = tk.Frame(self.content, bg="white")
        input_frame.pack(fill="x", padx=10, pady=10)

        tk.Label(input_frame, text="Mã SV:", font=("Segoe UI", 10)).pack(side="left", padx=5)
        self.tn_ma_sv = tk.Entry(input_frame, font=("Segoe UI", 10), width=15)
        self.tn_ma_sv.pack(side="left", padx=5)
        tk.Button(input_frame, text="Xét tốt nghiệp",
                 command=self.xet_tot_nghiep,
                 bg="#4CAF50", fg="white", relief="flat",
                 cursor="hand2").pack(side="left", padx=5)

        self.tn_result = tk.Frame(self.content, bg="white")
        self.tn_result.pack(fill="both", expand=True, padx=10, pady=10)

    def xet_tot_nghiep(self):
        ma_sv = self.tn_ma_sv.get().strip()
        if not ma_sv:
            return
        result = api.get(f"/tot-nghiep/check/{ma_sv}")
        if result.get("success"):
            data = result["data"]
            msg = (f"Mã SV: {data['ma_sv']}\n"
                  f"GPA thang 10: {data['gpa_thang_10']}\n"
                  f"GPA thang 4: {data['gpa_thang_4']}\n"
                  f"Xếp loại: {data['xep_loai']}\n"
                  f"Tổng tín chỉ: {data['tong_tin_chi']}")
            messagebox.showinfo("Kết quả tốt nghiệp", msg)
        else:
            messagebox.showerror("Lỗi", result.get("message", "Lỗi"))

    def show_thong_bao(self):
        """Quản lý thông báo"""
        self.clear_content()

        header = tk.Frame(self.content, bg="white", height=50)
        header.pack(fill="x", padx=10, pady=(10, 0))

        tk.Label(header, text="Quản lý Thông báo",
                font=("Segoe UI", 14, "bold"),
                bg="white").pack(side="left", padx=10, pady=10)
        tk.Button(header, text="+ Tạo thông báo",
                 command=self.tao_thong_bao,
                 bg="#4CAF50", fg="white", relief="flat",
                 cursor="hand2").pack(side="right", padx=10)

        result = api.get("/thong-bao/")
        data = result.get("data", [])

        list_frame = tk.Frame(self.content, bg="white")
        list_frame.pack(fill="both", expand=True, padx=10, pady=10)

        if not data:
            tk.Label(list_frame, text="Chưa có thông báo",
                    font=("Segoe UI", 12), bg="white").pack(pady=50)
            return

        for tb in data:
            fr = tk.Frame(list_frame, bg="#fff", bd=1, relief="solid")
            fr.pack(fill="x", pady=2, padx=5)
            tk.Label(fr, text=f"Mã: {tb.get('MaTB', '')}",
                    font=("Segoe UI", 9, "bold"), bg="white").pack(anchor="w", padx=5)
            tk.Label(fr, text=tb.get('NoiDung', ''),
                    font=("Segoe UI", 10), bg="white").pack(anchor="w", padx=5, pady=2)
            tk.Label(fr, text=f"Ngày: {tb.get('created_at', '')} | Admin: {tb.get('ten_admin', 'N/A')}",
                    font=("Segoe UI", 8), fg="#666", bg="white").pack(anchor="w", padx=5, pady=2)

    def tao_thong_bao(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Tạo thông báo")
        center_window(dialog, 400, 300)
        dialog.configure(bg="white")

        tk.Label(dialog, text="Tạo Thông báo", font=("Segoe UI", 12, "bold"),
                bg="white").pack(pady=10)

        tk.Label(dialog, text="Nội dung:", bg="white").pack(anchor="w", padx=20)
        noi_dung = tk.Text(dialog, font=("Segoe UI", 10), height=6, width=40)
        noi_dung.pack(padx=20, pady=5)

        tk.Label(dialog, text="Gửi đến:", bg="white").pack(anchor="w", padx=20)
        gui_den = ttk.Combobox(dialog, values=["Tất cả SV", "Theo lớp", "Theo ngành"])
        gui_den.set("Tất cả SV")
        gui_den.pack(padx=20, pady=5)

        def submit():
            nd = noi_dung.get("1.0", tk.END).strip()
            if not nd:
                messagebox.showerror("Lỗi", "Nhập nội dung")
                return

            gd = "all"
            if gui_den.get() == "Theo lớp":
                gd = "lop"
            elif gui_den.get() == "Theo ngành":
                gd = "nganh"

            result = api.post("/thong-bao/", {"noi_dung": nd, "gui_den": gd})
            if result.get("success"):
                messagebox.showinfo("Thành công", "Đã tạo thông báo")
                dialog.destroy()
                self.show_thong_bao()
            else:
                messagebox.showerror("Lỗi", result.get("message", "Lỗi"))

        tk.Button(dialog, text="Gửi", command=submit,
                 bg="#4CAF50", fg="white", relief="flat",
                 cursor="hand2").pack(pady=10)

    def clear_content(self):
        for w in self.content.winfo_children():
            w.destroy()

    def add_item(self, title, endpoint):
        """Generic add dialog"""
        dialog = tk.Toplevel(self.root)
        dialog.title(f"Thêm {title}")
        center_window(dialog, 400, 320)
        dialog.configure(bg="white")

        tk.Label(dialog, text=f"Thêm {title} mới", font=("Segoe UI", 12, "bold"),
                bg="white").pack(pady=10)

        result = api.get(endpoint)
        # Get column hints from existing data
        columns = []
        if result.get("data") and len(result["data"]) > 0:
            columns = [k for k in result["data"][0].keys() if k not in ("MatKhau",)]
        else:
            defaults = {
                "Khoa": [("Mã Khoa", "MaKhoa", 2), ("Tên Khoa", "TenKhoa", 50)],
                "Ngành": [("Mã Ngành", "MaNganh", 4), ("Tên Ngành", "TenNganh", 50), ("Mã Khoa", "MaKhoa", 2)],
                "Lớp": [("Mã Lớp", "MaLop", 11), ("Tên Lớp", "TenLop", 50), ("Mã Ngành", "MaNganh", 4)],
                "Môn học": [("Mã MH", "MaMH", 7), ("Tên MH", "TenMH", 50), ("Số TC", "SoTinChi", 2)],
            }
            if title in defaults:
                for label, key, width in defaults[title]:
                    tk.Label(dialog, text=f"{label}:", bg="white", anchor="w").pack(anchor="w", padx=30)

        # Build form based on known entity fields
        fields_config = {
            "Khoa": [("Mã Khoa", "MaKhoa"), ("Tên Khoa", "TenKhoa")],
            "Ngành": [("Mã Ngành", "MaNganh"), ("Tên Ngành", "TenNganh"), ("Mã Khoa", "MaKhoa")],
            "Lớp": [("Mã Lớp", "MaLop"), ("Tên Lớp", "TenLop"), ("Mã Ngành", "MaNganh")],
            "Môn học": [("Mã MH", "MaMH"), ("Tên MH", "TenMH"), ("Số TC", "SoTinChi")],
        }

        entries = {}
        if title in fields_config:
            form_frame = tk.Frame(dialog, bg="white")
            form_frame.pack(fill="x", padx=20, pady=5)
            for label, key in fields_config[title]:
                fr = tk.Frame(form_frame, bg="white")
                fr.pack(fill="x", pady=4)
                tk.Label(fr, text=f"{label}:", width=14, bg="white", anchor="e").pack(side="left")
                e = tk.Entry(fr, font=("Segoe UI", 10))
                e.pack(side="right", fill="x", expand=True)
                entries[key] = e
        else:
            tk.Label(dialog, text="Form chưa hỗ trợ cho " + title,
                    bg="white").pack(pady=20)

        def submit():
            data = {k: e.get().strip() for k, e in entries.items()}
            # Convert PascalCase label-keys to snake_case API keys
            snake_map = {
                "MaKhoa": "ma_khoa", "TenKhoa": "ten_khoa",
                "MaNganh": "ma_nganh", "TenNganh": "ten_nganh",
                "MaLop": "ma_lop", "TenLop": "ten_lop",
                "MaMH": "ma_mh", "TenMH": "ten_mh",
                "SoTinChi": "so_tin_chi",
            }
            snake_data = {snake_map.get(k, k): v for k, v in data.items()}
            if "so_tin_chi" in snake_data:
                try:
                    snake_data["so_tin_chi"] = int(snake_data["so_tin_chi"])
                except:
                    messagebox.showerror("Lỗi", "Số tín chỉ phải là số nguyên")
                    return
            result = api.post(endpoint, snake_data)
            if result.get("success"):
                messagebox.showinfo("Thành công", f"Đã thêm {title}")
                dialog.destroy()
                self.show_crud(title, endpoint)
            else:
                messagebox.showerror("Lỗi", result.get("message", result.get("error", "Lỗi")))

        tk.Button(dialog, text="Lưu", command=submit,
                 bg="#4CAF50", fg="white", relief="flat",
                 cursor="hand2").pack(pady=10)

    def edit_item(self, title, endpoint, row):
        """Generic edit dialog — pre-populated"""
        dialog = tk.Toplevel(self.root)
        dialog.title(f"Sửa {title}")
        center_window(dialog, 400, 320)
        dialog.configure(bg="white")

        pk_key = list(row.keys())[0]
        pk_val = row[pk_key]

        tk.Label(dialog, text=f"Sửa {title}", font=("Segoe UI", 12, "bold"),
                bg="white").pack(pady=10)

        fields_config = {
            "Khoa": [("Mã Khoa", "MaKhoa", True), ("Tên Khoa", "TenKhoa", False)],
            "Ngành": [("Mã Ngành", "MaNganh", True), ("Tên Ngành", "TenNganh", False), ("Mã Khoa", "MaKhoa", False)],
            "Lớp": [("Mã Lớp", "MaLop", True), ("Tên Lớp", "TenLop", False), ("Mã Ngành", "MaNganh", False)],
            "Môn học": [("Mã MH", "MaMH", True), ("Tên MH", "TenMH", False), ("Số TC", "SoTinChi", False)],
        }

        entries = {}
        if title in fields_config:
            form_frame = tk.Frame(dialog, bg="white")
            form_frame.pack(fill="x", padx=20, pady=5)
            for label, key, readonly in fields_config[title]:
                fr = tk.Frame(form_frame, bg="white")
                fr.pack(fill="x", pady=4)
                tk.Label(fr, text=f"{label}:", width=14, bg="white", anchor="e").pack(side="left")
                e = tk.Entry(fr, font=("Segoe UI", 10))
                e.insert(0, str(row.get(key, "")))
                if readonly:
                    e.configure(state="readonly")
                e.pack(side="right", fill="x", expand=True)
                entries[key] = e
        else:
            tk.Label(dialog, text="Form chưa hỗ trợ cho " + title,
                    bg="white").pack(pady=20)

        def submit():
            data = {k: e.get().strip() for k, e in entries.items()}
            # Convert PascalCase label-keys to snake_case API keys
            snake_map = {
                "MaKhoa": "ma_khoa", "TenKhoa": "ten_khoa",
                "MaNganh": "ma_nganh", "TenNganh": "ten_nganh",
                "MaLop": "ma_lop", "TenLop": "ten_lop",
                "MaMH": "ma_mh", "TenMH": "ten_mh",
                "SoTinChi": "so_tin_chi",
            }
            snake_data = {snake_map.get(k, k): v for k, v in data.items()}
            if "so_tin_chi" in snake_data:
                try:
                    snake_data["so_tin_chi"] = int(snake_data["so_tin_chi"])
                except:
                    messagebox.showerror("Lỗi", "Số tín chỉ phải là số nguyên")
                    return
            result = api.put(endpoint + pk_val, snake_data)
            if result.get("success"):
                messagebox.showinfo("Thành công", f"Đã cập nhật {title}")
                dialog.destroy()
                self.show_crud(title, endpoint)
            else:
                messagebox.showerror("Lỗi", result.get("message", result.get("error", "Lỗi")))

        tk.Button(dialog, text="Lưu", command=submit,
                 bg="#1976D2", fg="white", relief="flat",
                 cursor="hand2").pack(pady=10)

    def delete_item(self, title, endpoint, pk):
        if messagebox.askyesno("Xác nhận", f"Xóa {title}?"):
            result = api.delete(endpoint + pk)
            if result.get("success"):
                messagebox.showinfo("Thành công", f"Đã xóa {title}")
                self.show_crud(title, endpoint)
            else:
                messagebox.showerror("Lỗi", result.get("message", "Lỗi"))

    def show_quan_tri(self):
        """Quản lý tài khoản quản trị"""
        self.clear_content()

        header = tk.Frame(self.content, bg="white", height=50)
        header.pack(fill="x", padx=10, pady=(10, 0))

        tk.Label(header, text="Quản lý Tài khoản Admin",
                font=("Segoe UI", 14, "bold"),
                bg="white").pack(side="left", padx=10, pady=10)

        tk.Button(header, text="+ Thêm Admin",
                 command=self.add_quan_tri,
                 bg="#4CAF50", fg="white", relief="flat",
                 cursor="hand2").pack(side="right", padx=10)

        result = api.get("/quan-tri/")
        if "error" in result:
            tk.Label(self.content, text=result["error"],
                    fg="red", bg="white").pack(pady=20)
            return

        data = result.get("data", [])
        if not data:
            tk.Label(self.content, text="Chưa có tài khoản admin",
                    font=("Segoe UI", 12), bg="white").pack(pady=50)
            return

        table_frame = tk.Frame(self.content, bg="white")
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)

        headers = list(data[0].keys())
        col_widths = [10, 25, 25, 12]
        for i, (h, w) in enumerate(zip(headers, col_widths)):
            tk.Label(table_frame, text=h, font=("Segoe UI", 10, "bold"),
                    bg="#1976D2", fg="white", relief="ridge",
                    width=w).grid(row=0, column=i, sticky="nsew", padx=1, pady=1)

        for row_idx, row in enumerate(data):
            for col_idx, key in enumerate(headers):
                val = str(row.get(key, ""))
                bg = "white" if row_idx % 2 == 0 else "#E3F2FD"
                tk.Label(table_frame, text=val[:30], font=("Segoe UI", 9),
                        bg=bg, relief="ridge", anchor="w",
                        width=col_widths[col_idx]).grid(
                    row=row_idx + 1, column=col_idx, sticky="nsew", padx=1, pady=1)
            # Action buttons
            btn_frame = tk.Frame(table_frame, bg=bg)
            btn_frame.grid(row=row_idx + 1, column=len(headers),
                         sticky="nsew", padx=1, pady=1)
            tk.Button(btn_frame, text="Sửa",
                     command=lambda r=row: self.edit_quan_tri(r),
                     font=("Segoe UI", 8), bg="#FFC107", relief="flat",
                     cursor="hand2").pack(side="left", padx=2)
            tk.Button(btn_frame, text="Xóa",
                     command=lambda r=row: self.delete_quan_tri(r),
                     font=("Segoe UI", 8), bg="#D32F2F", fg="white",
                     relief="flat", cursor="hand2").pack(side="left", padx=2)

    def add_quan_tri(self):
        """Add admin account dialog"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Thêm Admin")
        center_window(dialog, 400, 300)
        dialog.configure(bg="white")

        tk.Label(dialog, text="Thêm Tài khoản Admin", font=("Segoe UI", 12, "bold"),
                bg="white").pack(pady=10)

        fields = [
            ("Mã Admin:", "ma_qt"),
            ("Họ tên:", "ho_ten"),
            ("Email (đăng nhập):", "email"),
            ("Mật khẩu:", "password_hash"),
        ]
        entries = {}
        for label, key in fields:
            fr = tk.Frame(dialog, bg="white")
            fr.pack(fill="x", padx=20, pady=5)
            tk.Label(fr, text=label, width=16, bg="white", anchor="e").pack(side="left")
            show = "*" if key == "password_hash" else ""
            e = tk.Entry(fr, font=("Segoe UI", 10), show=show)
            e.pack(side="right", fill="x", expand=True)
            entries[key] = e

        def submit():
            data = {k: e.get().strip() for k, e in entries.items()}
            if not all(data.values()):
                messagebox.showerror("Lỗi", "Vui lòng điền đầy đủ thông tin")
                return
            # Backend expects password_hash key for password
            result = api.post("/quan-tri/", {
                "ma_qt": data["ma_qt"],
                "ho_ten": data["ho_ten"],
                "email": data["email"],
                "password_hash": data["password_hash"]
            })
            if result.get("success"):
                messagebox.showinfo("Thành công", "Đã thêm tài khoản admin")
                dialog.destroy()
                self.show_quan_tri()
            else:
                messagebox.showerror("Lỗi", result.get("message", result.get("error", "Lỗi")))

        tk.Button(dialog, text="Lưu", command=submit,
                 bg="#4CAF50", fg="white", relief="flat",
                 cursor="hand2").pack(pady=10)

    def edit_quan_tri(self, row):
        """Edit admin account dialog"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Sửa Admin")
        center_window(dialog, 400, 320)
        dialog.configure(bg="white")

        ma_admin = row.get("ma_qt", "")

        tk.Label(dialog, text="Sửa Tài khoản Admin", font=("Segoe UI", 12, "bold"),
                bg="white").pack(pady=10)

        fields = [
            ("Mã Admin:", "ma_qt", True),
            ("Họ tên:", "ho_ten", False),
            ("Email (đăng nhập):", "email", False),
            ("Mật khẩu mới:", "password_hash", False),
        ]
        entries = {}
        for label, key, readonly in fields:
            fr = tk.Frame(dialog, bg="white")
            fr.pack(fill="x", padx=20, pady=5)
            tk.Label(fr, text=label, width=20, bg="white", anchor="e").pack(side="left")
            e = tk.Entry(fr, font=("Segoe UI", 10))
            e.insert(0, str(row.get(key, "")))
            if readonly:
                e.configure(state="readonly")
            e.pack(side="right", fill="x", expand=True)
            entries[key] = e

        def submit():
            data = {k: e.get().strip() for k, e in entries.items()}
            if not data.get("ho_ten") or not data.get("email"):
                messagebox.showerror("Lỗi", "Họ tên và Email bắt buộc")
                return
            payload = {"ho_ten": data["ho_ten"], "email": data["email"]}
            if data.get("password_hash"):
                payload["password_hash"] = data["password_hash"]
            result = api.put(f"/quan-tri/{ma_admin}", payload)
            if result.get("success"):
                messagebox.showinfo("Thành công", "Đã cập nhật")
                dialog.destroy()
                self.show_quan_tri()
            else:
                messagebox.showerror("Lỗi", result.get("message", result.get("error", "Lỗi")))

        tk.Button(dialog, text="Lưu", command=submit,
                 bg="#1976D2", fg="white", relief="flat",
                 cursor="hand2").pack(pady=10)

    def delete_quan_tri(self, row):
        ma_admin = row.get("ma_qt", "")
        if not messagebox.askyesno("Xác nhận", f"Xóa admin {ma_admin}?"):
            return
        result = api.delete(f"/quan-tri/{ma_admin}")
        if result.get("success"):
            messagebox.showinfo("Thành công", "Đã xóa tài khoản")
            self.show_quan_tri()
        else:
            messagebox.showerror("Lỗi", result.get("message", result.get("error", "Lỗi")))


# ========== Student Dashboard ==========

class StudentDashboard(BaseDashboard):
    def __init__(self, root):
        self.ma_sv = api.user.get("ma_sv", "")
        super().__init__(root, "Sinh viên")

    def setup_ui(self):
        header = tk.Frame(self.root, bg="#1565C0", height=60)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(header, text="SINH VIÊN",
                font=("Segoe UI", 16, "bold"),
                bg="#1565C0", fg="white").pack(side="left", padx=20)

        tk.Label(header, text=f"Xin chào: {api.user.get('ho_ten', '')}",
                font=("Segoe UI", 10), bg="#1565C0", fg="#BBDEFB").pack(side="right", padx=20)
        tk.Button(header, text="Đăng xuất", command=self.logout,
                 bg="#D32F2F", fg="white", relief="flat",
                 cursor="hand2").pack(side="right", padx=10)

        main = tk.Frame(self.root)
        main.pack(fill="both", expand=True)

        sidebar = tk.Frame(main, bg="#2E7D32", width=200)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        nav_items = [
            ("Thông tin cá nhân", self.show_profile),
            ("Bảng điểm", self.show_transcript),
            ("GPA", self.show_gpa),
            ("Tốt nghiệp", self.show_tot_nghiep),
            ("Thông báo", self.show_thong_bao),
        ]

        tk.Label(sidebar, text="MENU", font=("Segoe UI", 10, "bold"),
                bg="#2E7D32", fg="#A5D6A7").pack(pady=15, padx=10)

        for text, cmd in nav_items:
            btn = self.create_nav_button(sidebar, text, cmd)
            btn.configure(bg="#388E3C")
            btn.pack(fill="x", padx=5, pady=2)

        self.content = tk.Frame(main, bg="#f5f5f5")
        self.content.pack(side="right", fill="both", expand=True)

        self.show_profile()

    def show_profile(self):
        self.clear_content()
        result = api.get(f"/sinh-vien/{self.ma_sv}")
        if result.get("success"):
            data = result["data"]
            sv = data.get("sinh_vien", {})

            info = [
                ("Mã SV:", sv.get("ma_sv", "")),
                ("Họ tên:", sv.get("ho_ten", "")),
                ("Email:", sv.get("email", "")),
                ("Ngày sinh:", sv.get("ngay_sinh", "")),
                ("Lớp:", data.get("lop", {}).get("ten_lop", "N/A") if data.get("lop") else "N/A"),
                ("Ngành:", data.get("nganh", {}).get("ten_nganh", "N/A") if data.get("nganh") else "N/A"),
            ]

            for label, value in info:
                fr = tk.Frame(self.content, bg="white")
                fr.pack(fill="x", padx=20, pady=2)
                tk.Label(fr, text=label, font=("Segoe UI", 10, "bold"),
                        width=15, bg="white", anchor="e").pack(side="left")
                tk.Label(fr, text=value, font=("Segoe UI", 10),
                        bg="white").pack(side="left", padx=10)

    def show_transcript(self):
        self.clear_content()
        tk.Label(self.content, text="BẢNG ĐIỂM",
                font=("Segoe UI", 14, "bold"), bg="white").pack(pady=10)

        result = api.get(f"/hoc-tap/diem/{self.ma_sv}")
        data = result.get("data", [])

        if not data:
            tk.Label(self.content, text="Chưa có điểm",
                    font=("Segoe UI", 12), bg="white").pack(pady=50)
            return

        table = tk.Frame(self.content, bg="white")
        table.pack(fill="both", expand=True, padx=20, pady=10)

        headers = ["STT", "Mã môn", "Tên môn", "Số TC", "Điểm"]
        widths = [5, 10, 25, 8, 8]
        for i, (h, w) in enumerate(zip(headers, widths)):
            tk.Label(table, text=h, font=("Segoe UI", 10, "bold"),
                    bg="#2E7D32", fg="white", relief="ridge",
                    width=w).grid(row=0, column=i, sticky="nsew", padx=1, pady=1)

        for row_idx, d in enumerate(data):
            values = [row_idx + 1, d.get("ma_mh", ""), d.get("ten_mh", ""),
                     str(d.get("so_tin_chi", "")), str(d.get("diem", ""))]
            for col_idx, val in enumerate(values):
                bg = "white" if row_idx % 2 == 0 else "#E8F5E9"
                tk.Label(table, text=str(val)[:25], font=("Segoe UI", 9),
                        bg=bg, relief="ridge", anchor="w",
                        width=widths[col_idx]).grid(row=row_idx + 1, column=col_idx,
                                                   sticky="nsew", padx=1, pady=1)

    def show_gpa(self):
        self.clear_content()
        result = api.get(f"/hoc-tap/gpa/{self.ma_sv}")
        if result.get("success"):
            data = result["data"]
            fr = tk.Frame(self.content, bg="white")
            fr.pack(pady=50)

            tk.Label(fr, text="KẾT QUẢ HỌC TẬP",
                    font=("Segoe UI", 16, "bold"),
                    bg="white").pack(pady=20)

            info = [
                ("GPA Thang 10:", f"{data['gpa_thang_10']:.2f}"),
                ("GPA Thang 4:", f"{data['gpa_thang_4']:.2f}"),
                ("Tổng tín chỉ:", str(data['tong_tin_chi'])),
                ("Số môn học:", str(data['so_mon'])),
            ]

            for label, value in info:
                row = tk.Frame(fr, bg="white")
                row.pack(fill="x", pady=5)
                tk.Label(row, text=label, font=("Segoe UI", 11),
                        width=15, bg="white").pack(side="left")
                tk.Label(row, text=value, font=("Segoe UI", 11, "bold"),
                        bg="white", fg="#2E7D32").pack(side="left")
        else:
            tk.Label(self.content, text="Chưa có dữ liệu",
                    font=("Segoe UI", 12), bg="white").pack(pady=50)

    def show_tot_nghiep(self):
        self.clear_content()
        result = api.get(f"/tot-nghiep/status/{self.ma_sv}")
        if result.get("success"):
            data = result["data"]
            fr = tk.Frame(self.content, bg="white")
            fr.pack(pady=50)

            tk.Label(fr, text="TRẠNG THÁI TỐT NGHIỆP",
                    font=("Segoe UI", 16, "bold"),
                    bg="white").pack(pady=20)

            if data.get("da_xet"):
                info = [
                    ("GPA:", f"{data['gpa']:.2f} / 4.0"),
                    ("Xếp loại:", data.get("xep_loai", "")),
                ]
            else:
                info = [
                    ("GPA hiện tại (thang 4):", f"{data.get('gpa_thang_4_hien_tai', 0):.2f}"),
                    ("Xếp loại dự kiến:", data.get("xep_loai_du_kien", "")),
                    ("Tín chỉ tích lũy:", str(data.get("tong_tin_chi", 0))),
                ]

            for label, value in info:
                row = tk.Frame(fr, bg="white")
                row.pack(fill="x", pady=5)
                tk.Label(row, text=label, font=("Segoe UI", 11),
                        width=25, bg="white").pack(side="left")
                tk.Label(row, text=value, font=("Segoe UI", 11, "bold"),
                        bg="white", fg="#1565C0").pack(side="left")

    def show_thong_bao(self):
        self.clear_content()
        tk.Label(self.content, text="THÔNG BÁO",
                font=("Segoe UI", 14, "bold"), bg="white").pack(pady=10)

        result = api.get("/thong-bao/my")
        if result.get("success"):
            data = result["data"]
            unread = data.get("unread_count", 0)
            tk.Label(self.content, text=f"Chưa đọc: {unread}",
                    font=("Segoe UI", 10), bg="white").pack(anchor="w", padx=20)

            for tb in data.get("thong_bao", []):
                fr = tk.Frame(self.content, bg="#fff" if tb.get("TrangThaiDoc") else "#FFF3E0",
                             bd=1, relief="solid")
                fr.pack(fill="x", pady=2, padx=20)
                tk.Label(fr, text=tb.get("NoiDung", ""),
                        font=("Segoe UI", 10), bg=fr["bg"]).pack(anchor="w", padx=10, pady=5)
                tk.Label(fr, text=f"Ngày: {tb.get('NgayGui', '')}",
                        font=("Segoe UI", 8), fg="#666", bg=fr["bg"]).pack(anchor="w", padx=10)

                if not tb.get("TrangThaiDoc"):
                    api.post(f"/thong-bao/read/{tb.get('MaTB')}")

    def clear_content(self):
        for w in self.content.winfo_children():
            w.destroy()


# ========== Main Entry Point ==========

if __name__ == "__main__":
    root = tk.Tk()
    LoginWindow(root)
    root.mainloop()

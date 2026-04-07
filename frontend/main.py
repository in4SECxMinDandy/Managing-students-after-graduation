"""Streamlit frontend for QLSVSDH."""
import streamlit as st
import requests

st.set_page_config(
    page_title="QLSVSDH - Quản lý SV Sau Đại học",
    page_icon=":graduation_cap:",
    layout="wide",
)

API_BASE = "http://localhost:8000"


# ---- Auth helpers ----
def login(username: str, password: str) -> tuple[dict | None, str | None]:
    """Returns (payload, error_message). error_message set when API unreachable or non-200."""
    try:
        resp = requests.post(
            f"{API_BASE}/auth/login",
            json={"username": username, "password": password},
            timeout=10,
        )
        if resp.status_code == 200:
            return resp.json(), None
        return None, None
    except requests.exceptions.ConnectionError:
        return None, f"Không kết nối được API tại {API_BASE}. Hãy chạy backend (uvicorn) trước."
    except requests.exceptions.Timeout:
        return None, "API phản hồi quá lâu (timeout)."
    except Exception as exc:
        return None, str(exc)


def get_headers() -> dict:
    if "token" not in st.session_state:
        return {}
    return {"Authorization": f"Bearer {st.session_state.token}"}


def api_get(path: str, params=None) -> list | dict | None:
    try:
        resp = requests.get(
            f"{API_BASE}{path}",
            headers=get_headers(),
            params=params or {},
            timeout=10,
        )
        if resp.status_code == 200:
            return resp.json()
        return None
    except Exception:
        return None


def api_post(path: str, data: dict) -> dict | None:
    try:
        resp = requests.post(
            f"{API_BASE}{path}",
            headers=get_headers(),
            json=data,
            timeout=10,
        )
        if resp.status_code in (200, 201):
            return resp.json()
        return None
    except Exception:
        return None


def api_put(path: str, data: dict) -> dict | None:
    try:
        resp = requests.put(
            f"{API_BASE}{path}",
            headers=get_headers(),
            json=data,
            timeout=10,
        )
        if resp.status_code == 200:
            return resp.json()
        return None
    except Exception:
        return None


# ---- Initialize session state ----
if "token" not in st.session_state:
    st.session_state.token = None
if "user" not in st.session_state:
    st.session_state.user = None
if "page" not in st.session_state:
    st.session_state.page = "Đăng nhập"


# ---- Login page ----
def render_login():
    st.title(":graduation_cap: Hệ thống Quản lý SV Sau Đại học")
    st.divider()
    with st.form("login_form"):
        st.subheader("Đăng nhập")
        username = st.text_input("Tên đăng nhập / Email")
        password = st.text_input("Mật khẩu", type="password")
        submitted = st.form_submit_button("Đăng nhập", use_container_width=True)
        if submitted:
            user, conn_err = login(username, password)
            if conn_err:
                st.error(conn_err)
            elif user:
                st.session_state.token = user["access_token"]
                st.session_state.user = user
                st.session_state.page = "Dashboard"
                st.rerun()
            else:
                st.error("Sai tên đăng nhập hoặc mật khẩu")


# ---- Dashboard ----
def render_dashboard():
    st.title(f"Xin chào, {st.session_state.user['ho_ten']}")
    st.caption(f"Vai trò: {st.session_state.user['role']}")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Sinh viên", "1,234")
    with col2:
        st.metric("Giảng viên", "156")
    with col3:
        st.metric("Học kỳ hiện tại", "HK2 2025-2026")


# ---- Admissions ----
def render_admissions():
    st.header("Tuyển sinh")
    tab1, tab2, tab3 = st.tabs(["Hồ sơ", "Phương thức xét tuyển", "Duyệt"])
    with tab1:
        profiles = api_get("/admissions/profiles") or []
        st.dataframe(profiles, use_container_width=True, hide_index=True)
    with tab2:
        apps = api_get("/admissions/applications") or []
        st.dataframe(apps, use_container_width=True, hide_index=True)
    with tab3:
        st.info("Chọn hồ sơ để duyệt")


# ---- Training ----
def render_training():
    st.header("Đào tạo")
    tab1, tab2, tab3, tab4 = st.tabs(["Lớp học phần", "Đăng ký", "Phân công", "Điểm"])
    with tab1:
        sections = api_get("/training/class-sections") or []
        st.dataframe(sections, use_container_width=True, hide_index=True)
    with tab2:
        enrollments = api_get("/training/enrollments") or []
        st.dataframe(enrollments, use_container_width=True, hide_index=True)
    with tab3:
        assignments = api_get("/training/assignments") or []
        st.dataframe(assignments, use_container_width=True, hide_index=True)
    with tab4:
        grades = api_get("/training/grades") or []
        st.dataframe(grades, use_container_width=True, hide_index=True)


# ---- Thesis ----
def render_thesis():
    st.header("Luận văn")
    tab1, tab2, tab3, tab4 = st.tabs(["Luận văn", "Đề cương", "Hội đồng", "Thù lao"])
    with tab1:
        theses = api_get("/thesis/theses") or []
        st.dataframe(theses, use_container_width=True, hide_index=True)
    with tab2:
        outlines = api_get("/thesis/outlines") or []
        st.dataframe(outlines, use_container_width=True, hide_index=True)
    with tab3:
        committees = api_get("/thesis/committees") or []
        st.dataframe(committees, use_container_width=True, hide_index=True)
    with tab4:
        stipends = api_get("/thesis/stipends") or []
        st.dataframe(stipends, use_container_width=True, hide_index=True)


# ---- Finance ----
def render_finance():
    st.header("Tài chính")
    tab1, tab2 = st.tabs(["Đơn giá tín chỉ", "Học phí"])
    with tab1:
        rates = api_get("/finance/tuition-rates") or []
        st.dataframe(rates, use_container_width=True, hide_index=True)
    with tab2:
        tuitions = api_get("/finance/tuitions") or []
        st.dataframe(tuitions, use_container_width=True, hide_index=True)


# ---- Support ----
def render_support():
    st.header("Hỗ trợ")
    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        ["Thông báo", "NCKH", "Quy định", "Tốt nghiệp", "Lịch thi"]
    )
    with tab1:
        announcements = api_get("/support/announcements") or []
        st.dataframe(announcements, use_container_width=True, hide_index=True)
    with tab2:
        research = api_get("/support/research") or []
        st.dataframe(research, use_container_width=True, hide_index=True)
    with tab3:
        regulations = api_get("/support/regulations") or []
        st.dataframe(regulations, use_container_width=True, hide_index=True)
    with tab4:
        graduations = api_get("/support/graduations") or []
        st.dataframe(graduations, use_container_width=True, hide_index=True)
    with tab5:
        exams = api_get("/support/exam-schedules") or []
        st.dataframe(exams, use_container_width=True, hide_index=True)


# ---- Main ----
def main():
    if not st.session_state.token:
        render_login()
        return

    role = st.session_state.user.get("role", "")

    with st.sidebar:
        st.write(f"**{st.session_state.user.get('ho_ten', '')}**")
        st.caption(f"Vai trò: {role}")
        st.divider()
        pages = []
        if role in ("admin", "super_admin"):
            pages += ["Dashboard", "Admissions", "Training", "Thesis", "Finance", "Support", "Users"]
        elif role == "khoa":
            pages += ["Dashboard", "Training", "Thesis", "Finance", "Support"]
        elif role == "giangvien":
            pages += ["Dashboard", "Training", "Thesis"]
        else:
            pages += ["Dashboard", "Training", "Thesis", "Finance", "Support"]
        selected = st.radio("Điều hướng", pages, index=pages.index(st.session_state.page) if st.session_state.page in pages else 0)
        st.divider()
        if st.button("Đăng xuất", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

    st.session_state.page = selected

    match selected:
        case "Dashboard":
            render_dashboard()
        case "Admissions":
            render_admissions()
        case "Training":
            render_training()
        case "Thesis":
            render_thesis()
        case "Finance":
            render_finance()
        case "Support":
            render_support()
        case "Users":
            st.header("Quản lý người dùng")
            tab_sv, tab_gv, tab_admin = st.tabs(["Sinh viên", "Giảng viên", "Quản trị"])
            with tab_sv:
                sv_list = api_get("/auth/students") or []
                st.dataframe(sv_list, use_container_width=True, hide_index=True)
            with tab_gv:
                gv_list = api_get("/auth/lecturers") or []
                st.dataframe(gv_list, use_container_width=True, hide_index=True)
            with tab_admin:
                admin_list = api_get("/auth/admins") or []
                st.dataframe(admin_list, use_container_width=True, hide_index=True)


if __name__ == "__main__":
    main()

"""
AttendVision - main entry point.

Run with:  streamlit run app.py

This file only handles: page config, DB init, the login gate, and routing
to the selected view. Each view lives in views/ and owns its own UI logic.
"""
import streamlit as st

import config
import database as db
import auth
from views import dashboard, students, subjects, attendance, history, reports, settings

st.set_page_config(page_title="AttendVision", page_icon="🎓", layout="wide")

db.init_db()
db.seed_demo_data()

NAV_ITEMS = {
    "Dashboard": dashboard,
    "Take Attendance": attendance,
    "Students": students,
    "Subjects": subjects,
    "Attendance History": history,
    "Reports": reports,
    "Settings": settings,
}


def render_login():
    st.title("🎓 AttendVision")
    st.caption("Smart, hour-wise attendance using computer vision.")

    with st.form("login_form"):
        identifier = st.text_input("Username (admin) or Email (faculty)")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login", type="primary")

    if submitted:
        user = auth.login(identifier.strip(), password)
        if user:
            st.session_state["user"] = user
            st.rerun()
        else:
            st.error("Invalid credentials.")

    with st.expander("Demo credentials"):
        st.code(
            f"Admin    → username: {config.ADMIN_USERNAME}  password: {config.ADMIN_PASSWORD}\n"
            "Faculty  → email: faculty@example.edu  password: faculty123",
            language="text",
        )


def render_app():
    user = st.session_state["user"]

    with st.sidebar:
        st.markdown("## 🎓 AttendVision")
        st.caption(f"{user['name']} · {user['role'].title()}")

        choice = st.radio("Navigate", list(NAV_ITEMS.keys()), label_visibility="collapsed")

        st.divider()
        if st.button("Logout"):
            # Make sure a running camera session is released before logging out.
            camera = st.session_state.get("attendance_camera")
            if camera is not None:
                camera.release()
            st.session_state.clear()
            st.rerun()

    NAV_ITEMS[choice].render()


def main():
    if "user" not in st.session_state:
        render_login()
    else:
        render_app()


if __name__ == "__main__":
    main()

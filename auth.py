"""
AttendVision - authentication.

Two kinds of accounts for this prototype:
  - The single admin account, from ADMIN_USERNAME / ADMIN_PASSWORD env vars.
  - Faculty accounts, stored (hashed) in the `faculty` table.
Both resolve to a dict placed in st.session_state["user"].
"""
import config
import database as db


def login(identifier: str, password: str):
    """identifier is a username (admin) or email (faculty).
    Returns a user dict on success, or None on failure."""
    if identifier == config.ADMIN_USERNAME and password == config.ADMIN_PASSWORD:
        return {"id": None, "name": "Administrator", "email": config.ADMIN_USERNAME,
                "role": "admin", "department": None}

    faculty = db.get_faculty_by_email(identifier)
    if faculty and db.verify_password(password, faculty["password_hash"]):
        return {"id": faculty["id"], "name": faculty["name"], "email": faculty["email"],
                "role": faculty["role"], "department": faculty["department"]}

    return None

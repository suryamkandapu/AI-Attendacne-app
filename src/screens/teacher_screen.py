import streamlit as st

from src.ui.base_layout import (
    style_background_dashboard,
    style_base_layout
)

from src.components.header import header_dashboard
from src.components.footer import footer_dashboard


def teacher_screen():

    style_background_dashboard()
    style_base_layout()

    if "teacher_login_type" not in st.session_state:
        st.session_state.teacher_login_type = "login"

    if st.session_state.teacher_login_type == "login":
        teacher_screen_login()

    elif st.session_state.teacher_login_type == "register":
        teacher_screen_register()


def teacher_screen_login():

    c1, c2 = st.columns(
        2,
        vertical_alignment="center",
        gap="large"
    )

    with c1:
        header_dashboard()

    with c2:
        if st.button(
            "Go back to Home",
            type="secondary",
            key="loginbackbtn"
        ):
            st.session_state["login_type"] = None
            st.rerun()

    st.header("Login using password")

    teacher_username = st.text_input(
        "Enter username",
        placeholder="ananyaroy",
        key="login_username"
    )

    teacher_pass = st.text_input(
        "Enter password",
        type="password",
        placeholder="Enter password",
        key="login_password"
    )

    st.divider()

    btn1, btn2 = st.columns(2)

    with btn1:
        if st.button(
            "Login",
            use_container_width=True
        ):
            st.success(
                f"Logging in as {teacher_username}"
            )

    with btn2:
        if st.button(
            "Register Instead",
            type="primary",
            use_container_width=True
        ):
            st.session_state.teacher_login_type = "register"
            st.rerun()

    footer_dashboard()


def teacher_screen_register():

    c1, c2 = st.columns(
        2,
        vertical_alignment="center",
        gap="large"
    )

    with c1:
        header_dashboard()

    with c2:
        if st.button(
            "Go back to Home",
            type="secondary",
            key="registerbackbtn"
        ):
            st.session_state["login_type"] = None
            st.session_state.teacher_login_type = "login"
            st.rerun()

    st.header("Register your teacher profile")

    teacher_username = st.text_input(
        "Enter username",
        placeholder="ananyaroy",
        key="reg_username"
    )

    teacher_name = st.text_input(
        "Enter full name",
        placeholder="Ananya Roy",
        key="reg_name"
    )

    teacher_pass = st.text_input(
        "Enter password",
        type="password",
        placeholder="Enter password",
        key="reg_password"
    )

    teacher_pass_confirm = st.text_input(
        "Confirm password",
        type="password",
        placeholder="Confirm password",
        key="reg_confirm_password"
    )

    st.divider()

    btn1, btn2 = st.columns(2)

    with btn1:
        if st.button(
            "Login Instead",
            use_container_width=True
        ):
            st.session_state.teacher_login_type = "login"
            st.rerun()

    with btn2:
        if st.button(
            "Register",
            type="primary",
            use_container_width=True
        ):
            if teacher_pass != teacher_pass_confirm:
                st.error("Passwords do not match")
            else:
                st.success(
                    f"Teacher account created for {teacher_name}"
                )

    footer_dashboard()
import streamlit as st
import streamlit.components.v1 as components


def css_import(file: str):
    """
    Import custom css from a file

    <style>.button {text: red;};</style>
    >>> css_import("web/style.css")
    """
    with open(file) as f:
        stylesheet = f.read()

    return st.markdown(f"<style>{stylesheet}</style>", unsafe_allow_html=True)


def radio_buttons_horizontal(label="", options=None):
    if options is None:
        options = ["Option1", "Option2", "Option3"]

    st.radio(label=label, options=options)
    st.write(
        "<style>div.row-widget.stRadio > div{flex-direction: row;}</style>",
        unsafe_allow_html=True,
    )


# -----------------------------
#
# Examples
#
# -----------------------------


def example_column_with_css():
    col1, col2, col3 = st.columns(3)
    col1.metric("Temperature", "70 F", "1.2 F")
    col2.metric("Wind", "9 mph", "-8%")
    col3.metric("Humidity", "86%", "4%")


def javascript_import():
    return components.html(
        """
    <script>
    const boxes = document.querySelectorAll('[class*="nav-link"]')
    boxes.forEach((e)=>{e.href = "#/"})
    </script>
    """,
        height=0,
        width=0,
    )

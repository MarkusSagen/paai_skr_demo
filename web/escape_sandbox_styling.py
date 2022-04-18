import streamlit as st
import streamlit.components.v1 as components

st.subheader("Escaping the IFrame sandbox")
st.button("Red")
st.button("Blue")
st.button("Green")
components.html(
    """
    <script>
    const elems = window.parent.document.querySelectorAll('.stButton > button')
    elems[0].style.backgroundColor = 'lightcoral'
    elems[1].style.backgroundColor = 'lightblue'
    elems[2].style.backgroundColor = 'lightgreen'
    </script>
    """,
    height=0,
    width=0,
)

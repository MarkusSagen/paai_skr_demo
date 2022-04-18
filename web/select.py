import streamlit as st


def _create_header(topic_info):
    keywords = topic_info["Words"].tolist()
    topics = topic_info["Topic"].tolist()
    return [f"Ämne {str(i)} - {keywords}" for i, keywords in zip(topics, keywords)]


def _decode_header(selection):
    return int(selection.replace("Ämne ", "").split(" ")[0])


def create_topic_index_selection(topic_info, label=""):
    selected_topic_index = _decode_header(
        st.selectbox(label, (_create_header(topic_info)))
    )
    return selected_topic_index

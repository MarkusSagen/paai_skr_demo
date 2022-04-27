import streamlit as st


def _create_header(topic_info):
    """Prints the topics in the drop down menu among all topics in sidebar."""
    keywords = topic_info["Words"].tolist()
    topics = topic_info["Topic"].tolist()
    return [f"#{str(i)}: {keywords}" for i, keywords in zip(topics, keywords)]


def _decode_header(selection):
    return int(selection.replace("#", "").replace(":", "").split(" ")[0])


def create_topic_index_selection(topic_info, label=""):
    selected_topic_index = _decode_header(
        st.selectbox(label, (_create_header(topic_info)))
    )
    return selected_topic_index

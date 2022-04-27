import os
from audioop import reverse
from optparse import Values
from pathlib import Path
from typing import List

import streamlit as st
from PIL import Image

# Our custom functions
from web.display import display_topics_by_paragraphs
from web.initialize import (
    get_df,
    get_probs,
    get_probs_index_by_topic,
    get_topic_info,
    get_topic_model,
    get_topics,
    get_topics_per_municipality,
    get_topics_per_region,
)
from web.select import create_topic_index_selection
from web.streamlit_util import css_import
from web.visualize import visualize_topics, visualize_topics_per_class

DATAFRAME_PATH = "biblioteksplaner.csv"
MODEL_PATH = "models/model_mp_30/"
TOPIC_INFO_COLUMNS = ["Topic", "Words", "Frequency"]


img = Image.open("./web/icon.png")
st.set_page_config(page_title="SKR Topic Discovery", page_icon=img, layout="wide")

# Define padding and columns
padding_left, main, padding_right = st.columns((1, 8, 1))

# Initialize
df = get_df(input_data=DATAFRAME_PATH)
topics = get_topics(model_path=MODEL_PATH)
probs = get_probs(model_path=MODEL_PATH)
probs_index_by_topic = get_probs_index_by_topic(model_path=MODEL_PATH)
topics_per_region = get_topics_per_region(model_path=MODEL_PATH)
topics_per_municipality = get_topics_per_municipality(model_path=MODEL_PATH)
topic_model = get_topic_model(model_path=MODEL_PATH)
topic_info = get_topic_info(model_path=MODEL_PATH)
num_probs = len(probs)
num_topics = len(topics)


plotly_config = {"displayModeBar": True}

# Sidebar and options
with st.sidebar:
    st.image(img)
    st.markdown(
        """
        Undersök vilka ämnen som omnämns i biblioteksplaner från Sveriges kommuner
        Biblioteksplanerna är hämtade från [KBs hemsida](https://www.kb.se/samverkan-och-utveckling/biblioteksutveckling/biblioteksplaner.html)
        """
    )
    st.markdown("-----------")

    # Choose first graphics
    st.markdown("### Visa graf")
    show_topics_per_region = st.checkbox("Antal regioner per ämne", value=True)
    show_topic_info = st.checkbox("Antal biblioteksplaner per ämne")
    show_topics_hierarcy = st.checkbox("Hur ämnesindelningen gjorts")
    st.markdown("-----------")

    # Show search and filter
    st.markdown("### Sök och filtrera i texten")
    # TODO: Move to selection
    c = st.container()
    # all = st.checkbox("Välj alla")
    # if all:
    #     selected_regions = c.multiselect(
    #         "Välj Regioner:",
    #         list(df["region"].unique()),
    #         list(df["region"].unique()),
    #     )
    # else:
    selected_regions = c.multiselect(
        "Välj regioner", list(df["region"].unique()), "Stockholm"
    )

    # Selections
    selected_topic_index = create_topic_index_selection(topic_info, label="Välj ämne")

    # Selections for metadata
    st.markdown("#### Visa metadata")
    show_region = st.checkbox("Region", value=True)
    show_municipality = st.checkbox("Kommun", value=True)
    show_split = st.checkbox("Stycke")
    show_topic_idx = st.checkbox("Ämne", value=True)
    show_probs = st.checkbox("Sannolikhet")
    st.markdown("-----------")
    st.markdown("<a href='#linkto_top'>Link to top</a>", unsafe_allow_html=True)
    st.markdown("<a href='#linkto_bottom'>Link to bottom</a>", unsafe_allow_html=True)


# Context of paragraphs for each topic
with main:
    st.markdown("<div id='linkto_top'></div>", unsafe_allow_html=True)
    # Show initial graphic
    if show_topics_per_region:
        st.header("Sök tematiskt i kommunernas biblioteksplaner")
        st.markdown(
            """
            De teman/ämnen som presenteras i rullgardinsmenyerna och denna applikation är framtagna med hjälp av
            AI/språkteknologi, genom så kallat oövervakat lärande (unsupervised learning).
            Ingen mänsklig hand har lagts vid den tematiska indelningen av textavsnitten i biblioteksplanerna.
            """
        )
        st.markdown(
            """
            Webbapplikationen är en första prototyp som vi gärna tar in synpunkter på.<br>
            Lämna dina synpunkter, frågor och kommentarer på webbapplikationen här:<br>

            ##### [Frågeformulär](https://forms.gle/T9QchwsKsUeBLFbz6)
            ----
            """,
            unsafe_allow_html=True,
        )
        visualize_topics(
            topic_model=topic_model,
            topics_per_region=topics_per_region,
            topic_info=topic_info,
            config=plotly_config,
        )
    if show_topic_info:
        st.header("Ämnen som beskrivs och hur ofta")
        st.plotly_chart(
            visualize_topics_per_class(
                topic_model=topic_model,
                topics_per_class=topic_info,
                topics=topic_info["Topic"].tolist(),
                top_n_topics=len(topic_info["Topic"]),
                reverse_order=True,
                hide_all_but_first=False,
                use_name=True,
                # TODO:
                # - Pass in text for header and aside
                # - Make the sidebar selection effect the visualization
            ),
            config=plotly_config,
        )
    if show_topics_hierarcy:
        st.header("Hur ämnena har delats upp")
        st.plotly_chart(topic_model.visualize_hierarchy(), use_container_width=True)

    st.header("Texter från varje ämnen")
    st.markdown("<a href='#linkto_bottom'>Link to bottom</a>", unsafe_allow_html=True)

    # Expand and show content
    with st.expander("Visa biblioteksplaner för respktive ämne", expanded=True):
        with st.spinner("Laddar..."):
            display_topics_by_paragraphs(
                df=df,
                probs_by_idx=probs_index_by_topic,
                topic_idx=selected_topic_index,
                probs=probs,
                filters={"region": selected_regions},
                options={
                    "display_metadata": {
                        "region": show_region,
                        "municipality": show_municipality,
                        "split": show_split,
                        "topic_idx": show_topic_idx,
                        "probs": show_probs,
                    }
                },
            )
    st.markdown("<div id='linkto_bottom'></div>", unsafe_allow_html=True)
    st.markdown("<a href='#linkto_top'>Link to top</a>", unsafe_allow_html=True)

# TODO: Metrics
# example_column_with_css()

# ---------
# Escape the sandbox
css_import("web/css/style.css")

st.markdown(
    f"""
    <style>
        section[data-testid="stSidebar"] .css-1adrfps  {{width: 26rem;}}
    </style>
""",
    unsafe_allow_html=True,
)

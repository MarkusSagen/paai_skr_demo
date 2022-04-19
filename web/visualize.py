from typing import List

import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from sklearn.preprocessing import normalize


# ---------------------
# Cache plots - More useful when used with different configs
@st.cache(hash_funcs={dict: lambda _: None})
def _make_fig(topic_model, topics_per_region, topic_info):
    cached_dict = {
        "per_regions": visualize_topics_per_class(
            topic_model=topic_model,
            topics_per_class=topics_per_region,
            top_n_topics=5,
            topics=sorted(topic_info["Topic"]),
            normalize_frequency=False,
        ),
    }
    return cached_dict


def visualize_topics(topic_model, topics_per_region, topic_info, config):
    charts = _make_fig(topic_model, topics_per_region, topic_info)
    st.plotly_chart(charts["per_regions"], use_container_width=True, config=config)


def visualize_topics_per_class(
    topic_model,
    topics_per_class: pd.DataFrame,
    top_n_topics: int = 10,
    topics: List[int] = None,
    normalize_frequency: bool = False,
    width: int = 1250,
    height: int = 900,
    # Added
    reverse_order=False,
    hide_all_but_first=True,
    use_name=False,
) -> go.Figure:
    """Visualize topics per class

    Helper class to visualize topics from a BERTopic model in streamlit
    """
    colors = [
        "#E69F00",
        "#56B4E9",
        "#009E73",
        "#F0E442",
        "#D55E00",
        "#0072B2",
        "#CC79A7",
    ]

    # Select topics
    if topics:
        selected_topics = topics
    elif top_n_topics:
        selected_topics = (
            topic_model.get_topic_freq().head(top_n_topics + 1)[1:].Topic.values
        )
    else:
        selected_topics = topic_model.get_topic_freq().Topic.values

    if reverse_order:
        selected_topics = selected_topics[::-1]

    # Prepare data
    topic_names = {
        key: value[:40] + "..." if len(value) > 40 else value
        for key, value in topic_model.topic_names.items()
    }
    topics_per_class["Name"] = topics_per_class.Topic.map(topic_names)
    data = topics_per_class.loc[topics_per_class.Topic.isin(selected_topics), :]

    # Add traces
    fig = go.Figure()
    for index, topic in enumerate(selected_topics):
        # # Starts by hiding all but the first topic
        if hide_all_but_first:
            if index == 0:
                visible = True
            else:
                visible = "legendonly"
        else:
            visible = True

        trace_data = data.loc[data.Topic == topic, :]
        topic_name = trace_data.Name.values[0]
        words = trace_data.Words.values
        if normalize_frequency:
            x = normalize(trace_data.Frequency.values.reshape(1, -1))[0]
        else:
            x = trace_data.Frequency
        fig.add_trace(
            go.Bar(
                y=trace_data.Name if use_name else trace_data.Class,
                x=x,
                visible=visible,
                marker_color=colors[index % 7],
                hoverinfo="text",
                name=topic_name,
                orientation="h",
                hovertext=[f"<b>Topic {topic}</b><br>Words: {word}" for word in words],
            )
        )

    # Styling of the visualization
    fig.update_xaxes(showgrid=True)
    fig.update_yaxes(showgrid=True)
    fig.update_layout(
        xaxis_title="Normalized Frequency" if normalize_frequency else "Frequency",
        yaxis_title="Class",
        title={
            "text": "<b>Topics per Class",
            "y": 0.95,
            "x": 0.40,
            "xanchor": "center",
            "yanchor": "top",
            "font": dict(size=22, color="Black"),
        },
        template="simple_white",
        width=width,
        height=height,
        hoverlabel=dict(bgcolor="white", font_size=16, font_family="Rockwell"),
        legend=dict(
            title="<b>Global Topic Representation",
        ),
        legend_traceorder="reversed" if reverse_order else "normal",
    )
    return fig

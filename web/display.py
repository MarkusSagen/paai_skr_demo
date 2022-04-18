from typing import Any, Dict, List, Optional

import numpy as np
import pandas as pd
import streamlit as st
from annotated_text import annotated_text
from web.my_annotated_text.util import annot, rem

OPTIONS_DICT = Optional[Dict[str, Dict[str, Any]]]


def create_display_options() -> Dict[str, Dict[str, Any]]:
    return {
        "display_metadata": {
            "region": True,
            "municipality": True,
            "split": True,
            "topic_idx": True,
            "probs": False,
        }
    }


def _display_keywords(keywords, color="#dd0700", border="1px solid #dd0700", **style):
    default_style = dict(
        overflow="hidden",
        background="transparent",
        border_radius=rem(0.33),
        padding=(rem(0.08), rem(0.3)),
        margin=(rem(0.25)),
    )

    for elem, styling in default_style.items():
        style[elem] = style.get(elem, styling)

    return annotated_text(
        *[
            annot(
                f"{word} ",
                "",
                color=color,
                border=border,
                **style,
            )
            for word in keywords
        ],
    )


def display_metadata(
    df: pd.DataFrame,
    idx: int,
    topic_idx: int,
    probs: Optional[np.ndarray] = None,
    options: OPTIONS_DICT = None,
):
    """Displays the annotations with metadata for every library plan.

    idx       - The index in the dataframe
    topic_idx - Which topic by number
    options   - Dict describing which fields to display
    """

    style = dict(
        background="transparent",
        border_radius=rem(0.33),
        padding=(rem(0.08), rem(0.3)),
        margin=(rem(0.25)),
    )

    index = str(df["idx"].iloc[idx])
    region = df["region"].iloc[idx]
    municipality = df["municipality"].iloc[idx]
    split_by_id = str(df["_split_id"].iloc[idx])
    p = probs[:, topic_idx] if probs is not None else None

    METADATA_ANNOT = {
        "region": {
            "text": f"{index.zfill(2)} {region}",
            "subtext": "Region",
            "color": "#dd0700",
            "border": "1px solid #dd0700",
        },
        "municipality": {
            "text": municipality,
            "subtext": "Kommun",
            "color": "#2a7edd",
            "border": "1px solid #2a7edd",
        },
        "split": {
            "text": split_by_id,
            "subtext": "Stycke",
            "color": "#2d973b",
            "border": "1px solid #2d973b",
        },
        "topic_idx": {
            "text": str(topic_idx),
            "subtext": "Ämne #",
            "color": "#9e00ddb2",
            "border": "1px solid #9e00ddb2",
        },
        "probs": {
            "text": str(p[idx] if p is not None else 1),
            "subtext": "p",
            "color": "#c4b300",
            "border": "1px solid #c4b300",
        },
    }

    if options is None:
        options = create_display_options()

    """
    background: rgba(255, 164, 33, 0.4);
    color: rgb(42, 126, 221);
    border: 1px solid rgb(42, 126, 221);
    border-radius: 0.33rem;
    padding: 0.125rem 0.5rem;
    overflow: hidden;
    """

    metadata = []
    for attrib, display in options["display_metadata"].items():
        if display:
            m = METADATA_ANNOT[attrib]
            metadata.append(
                annot(
                    m["text"],
                    m["subtext"],
                    color=m["color"],
                    border=m["border"],
                    **style,
                )
            )

    annotated_text(*metadata)


def display_content(
    df: pd.DataFrame,
    probs_by_idx: np.ndarray,
    topic_idx: int,
    probs=None,
    filters: Optional[Dict[str, List[str]]] = None,
    options: OPTIONS_DICT = None,
):

    """
    # Ideally chain conditions and regions together
    # Using `.isin` on list since it is easier to start with


    df.loc[
        (
            df["region"].isin(["Kalmar "])
            | (
                df["region"].isin(["Östergötland"])
                & df["municipality"].isin(["Ydre", "Mjölby"])
            )
        ),
        "content",
    ]
    """

    def filter_values(filters, key):
        """filters["region"] == ["Stockholm", "Värmland"̈́]"""
        default_values = list(df[key].unique())
        values = filters.get(key, default_values)
        return values

    content_indices = df.index[
        [
            df["region"].isin(filter_values(filters, key="region")),
        ]
    ].tolist()

    st.markdown("---------")
    for idx in probs_by_idx[:, topic_idx]:
        if idx not in content_indices:
            continue
        st.write(df["content"].iloc[idx])
        display_metadata(
            df=df, idx=idx, topic_idx=topic_idx, probs=probs, options=options
        )
        st.markdown("---------")


def display_topics_by_paragraphs(
    df: pd.DataFrame,
    probs_by_idx: np.ndarray,
    topic_idx: int = 0,
    probs=None,
    filters: Optional[Dict[str, List[str]]] = None,
    options: OPTIONS_DICT = None,
):

    display_content(
        df=df,
        probs_by_idx=probs_by_idx,
        topic_idx=topic_idx,
        probs=probs,
        filters=filters,
        options=options,
    )

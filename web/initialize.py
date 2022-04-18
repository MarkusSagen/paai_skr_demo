import logging

import numpy as np
import pandas as pd
import streamlit as st
from bertopic import BERTopic
from bertopic.backend._utils import select_backend
from sentence_transformers import SentenceTransformer

from topics.np import load_numpy

logging.getLogger(__name__).addHandler(logging.NullHandler())


def _filter_dataframe(df, column="Topic", values=None):
    if values is None:
        values = [-1]  # Remove this index
    return df[df[column].isin(values) == False]


def _sort_probabilities_by_topic(probs: np.ndarray):
    highest_probs_per_idx = []
    _shape = probs.shape
    num_vals = range(len(probs))
    num_topics = 1 if len(_shape) == 1 else _shape[1]
    for topic in range(num_topics):
        prob = probs[:, topic]
        probs_sorted = sorted(num_vals, reverse=True, key=lambda idx: prob[idx])
        highest_probs_per_idx.append(probs_sorted)

    return np.array(highest_probs_per_idx).T


def _remove_first_underline(df: pd.DataFrame, column: str = "Name"):
    df[column] = df.apply(lambda d: " ".join(d[column].split("_")[1:]), axis=1)
    return df


def replace_symbol(df: pd.DataFrame, column: str = "Name", find="", rep=""):
    df[column] = df.apply(lambda d: d[column].replace(find, rep), axis=1)
    return df


def _remove_underlines(df: pd.DataFrame, column: str = "Name"):
    df = _remove_first_underline(df, column=column)
    df = replace_symbol(df, column, "_", " ")
    return df


# -------


@st.cache(allow_output_mutation=True)
def get_df(input_data="biblioteksplaner.csv"):
    df = pd.read_csv(input_data)
    df = df.astype(str)
    df.drop(columns="meta", inplace=True)
    return df


@st.cache(allow_output_mutation=True)
def get_topics(model_path="models/model_mp_30/"):
    return load_numpy(model_path + "topics.npy", as_list=True)


@st.cache(allow_output_mutation=True)
def get_probs(model_path="models/model_mp_30/"):
    return load_numpy(model_path + "probs.npy", as_list=False)


@st.cache(allow_output_mutation=True)
def get_probs_index_by_topic(model_path="models/model_mp_30/"):
    probs = load_numpy(model_path + "probs.npy", as_list=False)
    return _sort_probabilities_by_topic(probs)


@st.cache(allow_output_mutation=True)
def get_topics_per_region(model_path="models/model_mp_30/"):
    topics_per_region = pd.read_csv(model_path + "topics_per_region.csv")
    return _filter_dataframe(topics_per_region)


@st.cache(allow_output_mutation=True)
def get_topics_per_municipality(model_path="models/model_mp_30/"):
    topics_per_municipality = pd.read_csv(model_path + "topics_per_municipality.csv")
    return _filter_dataframe(topics_per_municipality)


@st.cache(allow_output_mutation=True)
def get_topic_model(model_path="models/model_mp_30/"):
    # model = SentenceTransformer(model_path)  # , device="cpu")
    # logging.error("Loaded SentenceTransformer")
    # model = select_backend(sentence_model)
    logging.info("Loading BERTopic")
    topic_model = BERTopic.load(model_path + "model")  # , embedding_model=model)
    logging.info("Loaded BERTopic")
    return topic_model


@st.cache(allow_output_mutation=True)
def get_topic_info(model_path):
    # Columns = (Topic, Count, Name)
    topic_model = get_topic_model(model_path=model_path)
    df: pd.DataFrame = topic_model.get_topic_info()
    df = _remove_first_underline(df, "Name")
    df = _filter_dataframe(df)

    df = df[["Topic", "Name", "Count"]]  # original name from topic_info
    df.rename(
        columns={"Topic": "Topic", "Name": "Words", "Count": "Frequency"},
        inplace=True,
    )
    df.reset_index(inplace=True, drop=True)
    return df

import os
from glob import glob
from pathlib import Path
from typing import List, Union

import click
import hdbscan
import numpy as np
import pandas as pd
import pendulum
from bertopic import BERTopic
from nltk.corpus import stopwords
from sentence_transformers import SentenceTransformer
from sklearn.feature_extraction.text import CountVectorizer

os.environ["TOKENIZERS_PARALLELISM"] = "false"


def save_numpy(inputs: Union[List, np.ndarray], path: str):
    arr: np.ndarray = np.array(inputs) if isinstance(inputs, list) else inputs
    np.save(file=path, arr=arr)


@click.command()
@click.option(
    "--input_dataframe",
    default="biblioteksplaner.csv",
    type=click.File("r"),
)
@click.option("--output_dir", default="models", type=click.Path())
@click.option("--min_topic_size", default=10, type=click.INT)
@click.option("--min_samples", default=3, type=click.INT)
@click.option("--language", default="swedish", type=click.STRING)
@click.option("--cluster_selection_method", default="eom", type=click.STRING)
@click.option("--num_topics", default=30, type=click.INT)
@click.option("--model_name", default="kb", type=click.Path())  # TODO: ngram
@click.option("--calculate_probabilities", default=False, type=click.BOOL)
@click.option("--include_timestamp", default=False, type=click.BOOL)
def create(
    input_dataframe,
    output_dir,
    min_topic_size,
    min_samples,
    language,
    cluster_selection_method,
    num_topics,
    model_name,
    calculate_probabilities,
    include_timestamp,
):
    df = pd.read_csv(input_dataframe)
    models = {
        "kb": "KBLab/sentence-bert-swedish-cased",
        "mp": "paraphrase-multilingual-mpnet-base-v2",
        "minilm": "paraphrase-multilingual-MiniLM-L12-v2",
    }

    hdbscan_model = hdbscan.HDBSCAN(
        min_cluster_size=min_topic_size,
        min_samples=min_samples,
        metric="euclidean",
        cluster_selection_method=cluster_selection_method,
        prediction_data=True,
    )

    # Filter the displayed topic names by number of names
    stop_words = stopwords.words(language)
    if language == "swedish":
        stop_words.extend(["per", "ska"])

    # TODO: Include lemmatization
    # https://github.com/MaartenGr/BERTopic/issues/286
    # https://stanfordnlp.github.io/stanza/lemma.html

    vectorizer_model = CountVectorizer(
        ngram_range=(1, 5),
        stop_words=stop_words,
    )

    topic_model = BERTopic(
        embedding_model=SentenceTransformer(models[model_name]),
        hdbscan_model=hdbscan_model,
        language=language,
        nr_topics=num_topics,
        vectorizer_model=vectorizer_model,
        calculate_probabilities=calculate_probabilities,
        verbose=True,
    )

    topics, probs = topic_model.fit_transform(df["content"])
    print(topic_model.get_topic_info())

    with open("converted_models_record.txt", "a+") as f:
        trained_with_args = f"Topic model: {model_name}, num_topics: {num_topics}, min_topic_size: {min_topic_size}, min_samples: {min_samples}"
        df_str = topic_model.get_topic_info().to_string(header=False, index=False)
        f.write(trained_with_args)
        f.write(df_str)
        f.write("")

    # %%
    # TODO: Add for year
    def get_topics_per_class(docs: pd.DataFrame, classes: pd.DataFrame):
        """Input dont have to be list, can be columns as well"""
        return topic_model.topics_per_class(
            docs=list(docs.values),
            topics=topics,
            classes=list(classes.values),
            global_tuning=True,
        )

    # %%
    print("Get topic per regions and municipality")
    topics_per_region = get_topics_per_class(df["content"], df["region"])
    topics_per_municipality = get_topics_per_class(df["content"], df["municipality"])

    # %%
    print("\nsaving model")
    model_path = f"{output_dir}/model_{model_name}_{num_topics}"
    if include_timestamp:
        current_time = str(pendulum.now()).split(".")[0]
        model_path += f"model_{current_time}"
    Path(model_path).mkdir(parents=True, exist_ok=True)

    # Needed for loading and using on CPU
    topic_model.save(f"{model_path}/model", save_embedding_model=False)

    save_numpy(topics, f"{model_path}/topics.npy")
    save_numpy(probs, f"{model_path}/probs.npy")

    topics_per_region.to_csv(f"{model_path}/topics_per_region.csv", index=False)
    topics_per_municipality.to_csv(
        f"{model_path}/topics_per_municipality.csv", index=False
    )

    print(f"Saved model to path:\n==> {model_path}")


if __name__ == "__main__":
    create()

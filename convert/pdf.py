import glob
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import pandas as pd
import pendulum
from haystack.nodes import (
    DocxToTextConverter,
    PDFToTextConverter,
    PreProcessor,
    TextConverter,
)

FILES_ROOT = "biblioteksplaner"
DATAFRAME_PATH = f"{FILES_ROOT}.csv"
SPAM_LINK_TEXT = " Länk till annan webbplats, öppnas i nytt fönster"

filepaths = glob.glob(f"./{FILES_ROOT}/**/*.pdf")
# + glob.glob("./biblioteksplaner/**/*.doc")
# + glob.glob("./biblioteksplaner/**/*.docx")

REGION_IDX = {
    "Region Stockholm": "01",
    "Region Uppsala": "03",
    "Region Sörmland": "04",
    "Region Östergötland": "05",
    "Region Jönköpings län": "06",
    "Region Kronoberg": "07",
    "Region Kalmar län": "08",
    "Region Gotland": "09",
    "Region Blekinge": "10",
    "Region Skåne": "12",
    "Region Halland": "13",
    "Västra Götalandsregionen": "14",
    "Region Värmland": "17",
    "Region Örebro län": "18",
    "Region Västmanland": "19",
    "Region Dalarna": "20",
    "Region Gävleborg": "21",
    "Region Västernorrland": "22",
    "Region Jämtland Härjedalen": "23",
    "Region Västerbotten": "24",
    "Region Norrbotten": "25",
}


@dataclass
class Metadata:
    region: str
    municipality: str
    file_type: str
    idx: str = field(default="")
    year_start: str = field(default="")
    year_end: str = field(default="")
    extracted_date: str = field(default="")
    region_size: str = field(default="")


class FileTypeError(Exception):
    def __init__(self, msg="Incorrect filetype", value=None):
        self.msg = msg
        self.value = value
        super().__init__(self.msg)

    def __repr__(self):
        return self.msg + self.value


def remove_trailing_year(text: str):
    """
    Kalmar 2021-2024 --> Kalmar
    """
    return " ".join(text.split(" ")[0:-1])


def clean_region_names(region: str):
    cleaned_text = (
        "".join(region)
        .split("_")[1]
        .replace("Region", "")
        .replace("regionen", "")
        .replace("Götalands", "Götaland")
        .replace("län", "")
        .replace("\xa0", " ")
        .replace("  ", " ")
        .strip()
    )
    return remove_trailing_year(cleaned_text)


def get_region_idx(region: str) -> str:
    idx = ""
    for region_full_name, region_idx in REGION_IDX.items():
        if region in region_full_name:
            idx = region_idx
    return idx


def clean_str(paragraph: str):
    return (
        paragraph.replace("•", "")
        .replace(".\n", ". ")  # Added
        .replace("\n", " ")
        .replace("", "")
        .replace("   ", "")
        .replace("  ", "")
        .replace("..", "")
        .replace("__", "")
    )


def create_metadeta(file_path: str) -> Metadata:
    current_time = str(pendulum.now()).split(".")[0]
    _base_foldername, _filename = "".join(file_path.split(FILES_ROOT))[1:].split("/")[
        2:
    ]

    region = clean_region_names(_base_foldername)
    if "Skåne" in region:
        region = region.split(" ")[0]

    idx = get_region_idx(region)

    file_splits = _filename.replace(SPAM_LINK_TEXT, "").split(".")
    # Happens if KB include local download links on their website (Danderyd)
    municipality = file_splits[0].split(" Pdf,")[0]
    file_type = file_splits[-1]

    return Metadata(
        region=region,
        municipality=municipality,
        file_type=file_type,
        idx=idx,
        extracted_date=current_time,
    )


def get_doc_keys() -> List[str]:
    return [
        "content",
        "content_type",
        "meta",
        "region",
        "municipality",
        "file_type",
        "idx",
        "year_start",
        "year_end",
        "extracted_date",
        "region_size",
        "_split_id",
    ]


def create_doc_dict() -> Dict[str, List[str]]:
    return {k: [] for k in get_doc_keys()}


def add_docs_to_dict(d: Dict[str, List[str]], document_dict: Dict[str, List[str]]):
    for k, v in d.items():
        if k == "meta":
            for param_k, param_v in d["meta"].items():
                document_dict[param_k].append(param_v)
        document_dict[k].append(v)
    return document_dict


class Converter:
    def __init__(self) -> None:
        self.pdf_converter = PDFToTextConverter().convert
        self.docx_converter = DocxToTextConverter().convert
        self.txt_converter = TextConverter().convert
        self._converter = {
            "pdf": self.pdf_converter,
            "docx": self.docx_converter,
            "txt": self.txt_converter,
        }

    def _check_filetype(self, file_path):
        if ".pdf" in file_path:
            return "pdf"
        elif ".docx" or ".doc" in file_path:
            return "docx"
        else:
            raise FileTypeError("Could not parse filetype in: ", file_path)

    def convert(
        self,
        file_path: Path,
        meta: Optional[Dict[str, str]] = None,
        remove_numeric_tables: Optional[bool] = None,
        valid_languages: Optional[List[str]] = None,
        encoding: Optional[str] = None,
        **kwargs,
    ):
        _convert = self._converter[self._check_filetype(file_path=file_path)]
        return _convert(
            file_path=file_path,
            meta=meta,
            remove_numeric_tables=remove_numeric_tables,
            valid_languages=valid_languages,
            encoding=encoding,
            **kwargs,
        )


class ProcessText:
    """
    word: {
        clean_empty_lines=True,
        clean_whitespace=True,
        clean_header_footer=False,
        split_by="word",
        split_length=100,
        split_respect_sentence_boundary=True,
    }

    sentences: {
        clean_empty_lines=True,
        clean_whitespace=True,
        clean_header_footer=True,
        split_by="sentence",
        split_length=4,
        split_overlap=0,
        split_respect_sentence_boundary=False,
        language="swedish",
    }
    """

    def __init__(
        self,
        clean_whitespace: bool = True,
        clean_header_footer: bool = False,
        clean_empty_lines: bool = True,
        split_by: str = "sentence",
        split_length: int = 4,
        split_overlap: int = 0,
        split_respect_sentence_boundary: bool = False,
        remove_substring=[],
        language="swedish",
        **kwargs,
    ):
        self.preprocessor = PreProcessor(
            clean_whitespace=clean_whitespace,
            clean_header_footer=clean_header_footer,
            clean_empty_lines=clean_empty_lines,
            split_by=split_by,
            split_length=split_length,
            split_overlap=split_overlap,
            split_respect_sentence_boundary=split_respect_sentence_boundary,
            remove_substrings=remove_substring,
            language=language,
        )

    def split(
        self,
        document: Dict[str, Any],
        split_by: str = "sentence",
        split_length: int = 5,
        split_overlap: int = 0,
        split_respect_sentence_boundary: bool = False,
    ):
        return self.preprocessor.split(
            document=document,
            split_by=split_by,
            split_length=split_length,
            split_overlap=split_overlap,
            split_respect_sentence_boundary=split_respect_sentence_boundary,
        )

    def process(
        self,
        documents: Tuple[Dict[str, Any], List[Dict[str, Any]]],
    ):
        return self.preprocessor.process(
            documents=documents,
        )


if __name__ == "__main__":

    processor_params = dict(
        clean_whitespace=True,
        clean_header_footer=True,
        clean_empty_lines=True,
        split_by="sentence",
        split_length=5,
        split_overlap=1,
        split_respect_sentence_boundary=False,
        remove_substring=[],
        language="swedish",
    )

    converter = Converter()
    preprocessor = ProcessText(**processor_params)

    libray_plans = []
    document_dict = create_doc_dict()
    for _, file_path in enumerate(filepaths):

        meta = create_metadeta(file_path=file_path)
        converter_params = dict(
            meta=meta.__dict__,
            remove_numeric_tables=True,
            valid_languages=["sv", "se", "en", "de"],
            encoding="UTF-8",
        )
        doc = converter.convert(file_path=file_path, **converter_params)
        docs = preprocessor.process(doc)

        for d in docs:
            d["content"] = clean_str(d["content"])
            document_dict = add_docs_to_dict(d, document_dict)

    df = pd.DataFrame(document_dict)
    df.to_csv(DATAFRAME_PATH, index=False)

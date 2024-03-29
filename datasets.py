from dataclasses import asdict, dataclass
from typing import Literal, NamedTuple, Self, cast, get_args

__all__: list[str] = ["Dataset"]
TDatasetType = Literal["density", "viscosity", "surften"]


@dataclass
class DatasetDetails:
    """Represents the details of a dataset in dictionary form."""

    measurement_method: str | None
    water_content_ppm: int | None
    sample_supplier: str | None
    purification_method: str | None


class DataPoint(NamedTuple):
    """Represents a single data point in a dataset."""

    temperature_K: float
    pressure_MPa: float
    value: float


@dataclass
class Dataset:
    """Represents a single dataset."""

    type: Literal["density", "viscosity", "surften"]
    accepted: bool
    reference: str
    ionic_liquid: str
    details: DatasetDetails
    data: list[DataPoint]

    @classmethod
    def from_text(cls, text: str) -> Self:
        """Convert a text representing a single dataset into the `Dataset` instance."""

        text_list = text.split("\n")
        if len(text_list) < 7:
            raise ValueError(
                f"Text has too few rows. Expected >7, got {len(text_list)}"
            )
        if text_list[0][-1] == "*":
            accepted = False
            text_list[0] = text_list[0].replace("*", "")
        else:
            accepted = True
        type_ = (text_list[0].split(":"))[1].strip()
        type_ = cast(TDatasetType, type_)
        if type_ not in list(get_args(TDatasetType)):
            raise ValueError(
                f"Invalid 'type' value: {type_}. "
                f"Expected one of 'density', 'viscosity', 'surften'."
            )
        reference = text_list[1]
        ionic_liquid = text_list[4]
        if (text_list[5].split(";"))[1].isdigit():
            water_content_ppm = int((text_list[5].split(";"))[1])
        else:
            water_content_ppm = None
        details = DatasetDetails(
            measurement_method=(text_list[5].split(";"))[0],
            water_content_ppm=water_content_ppm,
            sample_supplier=(text_list[5].split(";"))[2],
            purification_method=(text_list[5].split(";"))[3],
        )
        data = []
        for row in text_list[6:]:
            row_values = list(map(float, row.split(" ")))
            dp = DataPoint(row_values[0], row_values[1], row_values[2])
            data.append(dp)
        return cls(type_, accepted, reference, ionic_liquid, details, data)

    @classmethod
    def from_file(cls, file_path: str) -> list[Self]:
        """Convert a file containing multiple datasets into a list of `Dataset`
        instances.
        """
        with open(file_path, "r") as file:
            file_data = [x for x in file.read().split("\n\n") if x != ""]
            if file_data[-1][-1] == "\n":
                file_data[-1] = file_data[-1][:-1]
        datasets_collector: list[Self] = []
        for text in file_data:
            try:
                datasets_list = cls.from_text(text)
                datasets_collector.append(datasets_list)
            except Exception as e:
                print(f"Skipping dataset due to following error: {str(e)}")
        return datasets_collector

    @classmethod
    def to_dict(cls, dataset: Self) -> dict:
        ds_dict = asdict(dataset)
        ds_dict["data"] = [x._asdict() for x in ds_dict["data"]]
        return ds_dict

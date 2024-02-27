from dataclasses import dataclass
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
        if len(text_list) < 6:
            raise ValueError(
                f"Text has too few rows. Expected >6, got {len(text_list)}"
            )
        if text_list[0][-1] == "*":
            accepted = False
            text = text.replace("*", "")
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
        raise NotImplementedError

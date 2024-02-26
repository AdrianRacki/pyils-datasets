from dataclasses import dataclass
from typing import Literal, NamedTuple, Self

__all__: list[str] = ["Dataset"]


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
        """Convert a text representing a single dataset into the `Dataset` instance.

        Args:
            text (str): String with specific pattern in which each row is separated
                by "\n"

        Raises:
            Exception: Input text does not have enough rows to assign values to
                all attributes of the Dataset class.

        Returns:
            Self: Returns Dataset class object with data imported from input text.
        """
        if text.find("*") != -1:
            accepted = False
            text = text.replace("*", "")
        else:
            accepted = True
        text_list = text.split("\n")
        if len(text_list) < 6:
            raise Exception(f"Text has too few rows. Expected >6, got {len(text_list)}")
        elif len(text_list) < 7:
            print("Warning: No data to import! Check input.")
        type = (text_list[0].split(":"))[1].strip()
        if type not in ("density", "viscosity", "surften"):
            raise ValueError(
                f"Invalid 'type' value: {type}. "
                f"Expected one of 'density', 'viscosity', 'surften'."
            )
        reference = text_list[1]
        ionic_liquid = text_list[4]
        try:
            water_content_ppm = int((text_list[5].split(";"))[1])
        except:  # noqa: E722
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
            dp = DataPoint(*row_values)
            data.append(dp)
        return cls(
            type=type,
            accepted=accepted,
            reference=reference,
            ionic_liquid=ionic_liquid,
            details=details,
            data=data,
        )

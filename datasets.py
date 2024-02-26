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
        """Convert a text representing a single dataset into the `Dataset` instance."""
        raise NotImplementedError

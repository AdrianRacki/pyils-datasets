import pytest

from datasets import Dataset, DatasetDetails


def test_dataset_from_text_returns_dataset_instance_from_valid_text() -> None:
    # Arrange.
    text = """
    dataset:density
    kanakubo-2015
    1
    mole
    im-6,1_ntf2
    dilatometer;30;synthesis;vacuum drying
    288.15 14.95 1393.3
    288.15 20.18 1396.8
    288.15 25.08 1400
    288.15 30.1 1403.2
    288.15 40.12 1409.5
    288.15 49.94 1415.3
    288.15 75.5 1429.5
    288.16 100 1442.2
    288.15 124.7 1453.9
    288.16 150.5 1465
    288.15 174.6 1474.9
    """

    # Prepare raw text for parsing.
    text = "\n".join(filter(None, map(str.strip, text.split("\n"))))

    # Act.
    dataset = Dataset.from_text(text)

    # Assert.
    assert dataset.type == "density"
    assert dataset.accepted is True
    assert dataset.reference == "kanakubo-2015"
    assert dataset.ionic_liquid == "im-6,1_ntf2"
    assert dataset.details == DatasetDetails(
        measurement_method="dilatometer",
        water_content_ppm=30,
        sample_supplier="synthesis",
        purification_method="vacuum drying",
    )
    assert dataset.data == [
        (288.15, 14.95, 1393.3),
        (288.15, 20.18, 1396.8),
        (288.15, 25.08, 1400.0),
        (288.15, 30.10, 1403.2),
        (288.15, 40.12, 1409.5),
        (288.15, 49.94, 1415.3),
        (288.15, 75.50, 1429.5),
        (288.16, 100.0, 1442.2),
        (288.15, 124.7, 1453.9),
        (288.16, 150.5, 1465.0),
        (288.15, 174.6, 1474.9),
    ]


def test_dataset_from_text_raises_value_error_when_data_are_not_found() -> None:
    # Arrange.
    text = """
    dataset:density
    kanakubo-2015
    1
    mole
    im-6,1_ntf2
    dilatometer;30;synthesis;vacuum drying
    """

    # Prepare raw text for parsing.
    text = "\n".join(filter(None, map(str.strip, text.split("\n"))))

    # Assert.
    with pytest.raises(ValueError):
        Dataset.from_text(text)


def test_dataset_from_text_raises_value_error_when_data_has_wrong_type() -> None:
    # Arrange.
    text = """
    dataset:densiity
    kanakubo-2015
    1
    mole
    im-6,1_ntf2
    dilatometer;30;synthesis;vacuum drying
    288.15 14.95 1393.3
    288.15 20.18 1396.8
    """

    # Prepare raw text for parsing.
    text = "\n".join(filter(None, map(str.strip, text.split("\n"))))

    # Assert.
    with pytest.raises(ValueError):
        Dataset.from_text(text)


def test_dataset_from_text_returns_dataset_from_text_with_asterisk() -> None:
    # Arrange.
    text = """
    dataset:density*
    kanakubo-2015
    1
    mole
    im-6,1_ntf2
    dilatometer;not stated;synthesis;vacuum drying
    288.15 14.95 1393.3
    """

    # Prepare raw text for parsing.
    text = "\n".join(filter(None, map(str.strip, text.split("\n"))))

    # Act.
    dataset = Dataset.from_text(text)

    # Assert.
    assert dataset.type == "density"
    assert dataset.accepted is False
    assert dataset.reference == "kanakubo-2015"
    assert dataset.ionic_liquid == "im-6,1_ntf2"
    assert dataset.details == DatasetDetails(
        measurement_method="dilatometer",
        water_content_ppm=None,
        sample_supplier="synthesis",
        purification_method="vacuum drying",
    )
    assert dataset.data == [(288.15, 14.95, 1393.3)]

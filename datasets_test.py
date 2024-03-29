import os
import random

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


def test_dataset_from_file_reads_and_returns_list_of_datasets_from_file() -> None:
    # Arrange.
    file_path = "temp_data_file.dat"
    file_data = [
        """
        dataset:density
        ghanem-2015
        1
        mole
        im-8,1_gly
        U-tube;300;synthesis;vacuum drying
        293.15 0.1 1041.7
        303.15 0.1 1035.3
        313.15 0.1 1029.1
        323.15 0.1 1023
        333.15 0.1 1016.8
        343.15 0.1 1010.6
        353.15 0.1 1004.4
        363.15 0.1 998.6
        373.15 0.1 992.8
        """,
        """
        dataset:viscosity*
        yousefi-2017
        1
        mole
        im-8,1_gly
        Stabinger;500;synthesis;vacuum drying
        293.15 0.1 479.9
        298.15 0.1 342.1
        303.15 0.1 238.9
        313.15 0.1 135.4
        323.15 0.1 78.8
        333.15 0.1 49.4
        343.15 0.1 33.1
        353.15 0.1 24.19
        363.15 0.1 16.68
        """,
        """
        dataset:surften
        ghanem-2015
        1
        mole
        im-8,1_gly
        droplet;304;synthesis;vacuum drying
        293.15 0.1 35.37
        303.15 0.1 33.98
        313.15 0.1 32.81
        323.15 0.1 31.35
        333.15 0.1 30.07
        343.15 0.1 28.75
        353.15 0.1 27.42
        """,
    ]

    # Prepare raw text for parsing.
    file_data = [
        "\n".join(filter(None, map(str.strip, text.split("\n")))) for text in file_data
    ]

    with open(file_path, "w") as file:
        delimiters = [
            "\n\n" * random.randint(1, 3) for _ in range(len(file_data) - 1)
        ] + ["\n"]
        file_contents = ""

        for data, delimiter in zip(file_data, delimiters):
            file_contents += data + delimiter
        file.write(file_contents)

    # Act.
    try:
        datasets = Dataset.from_file(file_path)
    except Exception as e:
        raise e
    finally:
        os.remove(file_path)

    # Assert.
    assert datasets == [
        Dataset.from_text(file_data[0]),
        Dataset.from_text(file_data[1]),
        Dataset.from_text(file_data[2]),
    ]


def test_dataset_to_dict_returns_dict_from_dataset() -> None:
    # Arrange
    text = """
    dataset:density
    kanakubo-2015
    1
    mole
    im-6,1_ntf2
    dilatometer;30;synthesis;vacuum drying
    288.15 14.95 1393.3
    288.15 20.18 1396.8
    """
    test_dict = {
        "type": "density",
        "accepted": True,
        "reference": "kanakubo-2015",
        "ionic_liquid": "im-6,1_ntf2",
        "details": {
            "measurement_method": "dilatometer",
            "water_content_ppm": 30,
            "sample_supplier": "synthesis",
            "purification_method": "vacuum drying",
        },
        "data": [
            {"temperature_K": 288.15, "pressure_MPa": 14.95, "value": 1393.3},
            {"temperature_K": 288.15, "pressure_MPa": 20.18, "value": 1396.8},
        ],
    }
    text = "\n".join(filter(None, map(str.strip, text.split("\n"))))
    dataset = Dataset.from_text(text)

    # Act
    dataset_dict = Dataset.to_dict(dataset)

    # Assert
    assert dataset_dict == test_dict

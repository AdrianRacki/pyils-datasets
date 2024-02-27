import os

import pytest

from datasets import Dataset, DatasetDetails


@pytest.mark.xfail(reason="Not implemented yet.")
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
        file.write("\n\n".join(file_data))

    # Act.
    datasets = Dataset.from_file(file_path)

    os.remove(file_path)

    # Assert.
    assert datasets == [
        Dataset.from_text(file_data[0]),
        Dataset.from_text(file_data[1]),
        Dataset.from_text(file_data[2]),
    ]

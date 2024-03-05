import json
import os

from datasets import Dataset


def data_to_json(dir_source_path: str, target_path: str) -> None:
    """Merges all .dat files in source directory into single .json file."""
    target_path += ".json"
    data_collector = []
    for filename in os.listdir(dir_source_path):
        file_path = os.path.join(dir_source_path, filename)
        try:
            dataset_list = Dataset.from_file(file_path)
            dataset_dict_list = [Dataset.to_dict(x) for x in dataset_list]
            data_collector.extend(dataset_dict_list)
        except Exception as e:
            print(f"Skipping whole >{filename}< due to following error {str(e)}")
    with open(target_path, "w") as outfile:
        json.dump(data_collector, outfile)


data_to_json("dat", "data")

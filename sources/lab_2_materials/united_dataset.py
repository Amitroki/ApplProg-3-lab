import os
import shutil
import csv


from sources.lab_2_materials.default_dataset_operations import create_file


def make_folder(name: str) -> None:
    """
    This function create a new folder with specified by user name
    if it is not exist. If the folder exists, function do nothing
    """
    if not os.path.isdir(name):
        os.mkdir(name)


def copy_dataset(dataset: str) -> None:
    """
    This function create a copy of dataset with a specified name
    """
    make_folder("copied_dataset")
    animal_types = os.listdir(f"dataset")
    for animal_type in animal_types:
        animals = os.listdir(os.path.join("dataset", animal_type))
        for animal_photo in animals:
            shutil.copyfile(os.path.join(os.path.join("dataset", animal_type), animal_photo), os.path.join(
                "copied_dataset", f"{animal_type}_{animal_photo}"))


def input_data(file_name: str) -> None:
    """
    This function add file paths from folder into the created csv-file
    """
    full_path = os.path.abspath("copied_dataset")
    animals = os.listdir("copied_dataset")
    relative_path = os.path.relpath("copied_dataset")
    with open(file_name, "a", newline="") as file:
        file_writer = csv.writer(file, delimiter=",", lineterminator='\r')
        for animal in animals:
            file_writer.writerow(
                [os.path.join(full_path, animal),
                 os.path.join(relative_path, animal),
                 animal]
            )


def main() -> None:
    copy_dataset("dataset")
    create_file("annotation2.csv")
    input_data("annotation2.csv")


if __name__ == "__main__":
    main()

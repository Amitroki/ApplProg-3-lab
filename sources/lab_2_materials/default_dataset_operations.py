import os
import csv


def input_data(file_name: str, type: str) -> None:
    """
    This function add file paths from folder into the created csv-file
    """
    full_path = os.path.abspath("dataset")
    animals = os.listdir(os.path.join(full_path, type))
    relative_path = os.path.relpath("dataset")
    with open(file_name, "a", newline="") as file:
        file_writer = csv.writer(file, delimiter=",", lineterminator='\r')
        for animal in animals:
            file_writer.writerow(
                [os.path.join(full_path, type, animal),
                 os.path.join(relative_path, type, animal),
                 animal]
            )


def create_file(file_name: str) -> None:
    """
    This function create a new csv-file (or rewrite existed) with specified by user name
    """
    with open(file_name, 'w') as file:
        file_writer = csv.writer(file, delimiter=",", lineterminator="\r")
        file_writer.writerow(["Absolute path", "Relative path", "Type"])


def main() -> None:
    create_file("annotation1.csv")
    input_data("annotation1.csv", "bay_horse")
    input_data("annotation1.csv", "zebra")


if __name__ == "__main__":
    main()

import os
import shutil
import csv
from random import sample


from sources.lab_2_materials.united_dataset import create_file, make_folder


def copy_and_rename_dataset(default_dataset: str, new_dataset_name: str, csv_file_name: str) -> None:
    """
    This function create a copy of specified dataset
    """
    random_number = sample(list(range(10000)), 2000)
    make_folder(new_dataset_name)
    full_path = os.path.abspath(new_dataset_name)
    relative_path = os.path.relpath(new_dataset_name)
    animal_types = os.listdir(default_dataset)
    counter = 0
    for animal_type in animal_types:
        animals = os.listdir(os.path.join(default_dataset, animal_type))
        for animal_photo in animals:
            random_name = str(random_number[counter]).zfill(5)
            shutil.copyfile(os.path.join(os.path.join(default_dataset, animal_type), animal_photo),
                            os.path.join(new_dataset_name, random_name + ".jpg"))
            with open(f"{csv_file_name}.csv", 'a', newline='') as file:
                file_writer = csv.writer(
                    file, delimiter=",", lineterminator='\r')
                file_writer.writerow(
                    [os.path.join(full_path, random_name),
                     os.path.join(relative_path, random_name),
                     animal_type]
                )
                counter += 1


def main() -> None:
    if os.path.isdir("second_copied_dataset"):
        shutil.rmtree("second_copied_dataset")
    create_file("annotation3.csv")
    copy_and_rename_dataset()


if __name__ == "__main__":
    main()

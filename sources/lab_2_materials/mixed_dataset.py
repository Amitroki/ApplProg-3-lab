import os
import shutil
import csv
from random import sample


from sources.lab_2_materials.united_dataset import create_file, make_folder


def copy_and_rename_dataset() -> None:
    """
    This function create a copy of specified dataset
    """
    random_number = sample(list(range(10000)), 5000)
    make_folder("second_copied_dataset")
    full_path = os.path.abspath("second_copied_dataset")
    relative_path = os.path.relpath("second_copied_dataset")
    animal_types = os.listdir("dataset")
    counter = 0
    for animal_type in animal_types:
        animals = os.listdir(os.path.join("dataset", animal_type))
        for animal_photo in animals:
            random_name = str(random_number[counter]).zfill(5)
            shutil.copyfile(os.path.join(os.path.join("dataset", animal_type), animal_photo),
                            os.path.join("second_copied_dataset", random_name + ".jpg"))
            with open("annotation3.csv", 'a', newline='') as file:
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

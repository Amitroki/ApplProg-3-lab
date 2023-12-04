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


def copy_dataset(dataset: str, new_dataset_name: str) -> str:
    """
    This function create a copy of dataset with a specified name
    """
    make_folder(new_dataset_name)
    animal_types = os.listdir(dataset)
    for animal_type in animal_types:
        animals = os.listdir(os.path.join(dataset, animal_type))
        for animal_photo in animals:
            shutil.copyfile(
                os.path.join(os.path.join(dataset, animal_type), animal_photo), 
                os.path.join(new_dataset_name, f"{animal_type}_{animal_photo}")
            )
    return os.path.abspath(new_dataset_name)

def input_data(new_dataset_name: str, file_name: str) -> None:
    """
    This function add file paths from folder into the created csv-file
    """
    full_path = os.path.abspath(new_dataset_name)
    animals = os.listdir(new_dataset_name)
    counter = 0
    start = ""
    for i in new_dataset_name:
        if i == "/":
            counter += 1
        start += i
        if counter == 5:
            break
    relative_path = os.path.relpath(new_dataset_name, start)
    type = os.path.basename(os.path.normpath(new_dataset_name))
    with open(file_name, "a", newline="") as file:
        file_writer = csv.writer(file, delimiter=",", lineterminator='\r')
        for animal in animals:
            file_writer.writerow(
                [os.path.join(os.path.abspath(new_dataset_name), animal).replace("\\", "/"),
                 os.path.join(relative_path, animal).replace("\\", "/"),
                 type]
            )
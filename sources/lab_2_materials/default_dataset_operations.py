import os
import csv


def input_data(path_to_the_dataset: str, file_name: str) -> None:
    """
    This function add file paths from folder into the created csv-file
    """
    animals = os.listdir(path_to_the_dataset)
    #start = "C:/Users/Alex/Desktop/application_programming/"
    counter = 0
    start = ""
    for i in path_to_the_dataset:
        if i == "/":
            counter += 1
        start += i
        if counter == 5:
            break
    type = os.path.basename(os.path.normpath(path_to_the_dataset))
    relative_path = os.path.relpath(path_to_the_dataset, start)
    with open(file_name, "a", newline="") as file:
        file_writer = csv.writer(file, delimiter=",", lineterminator='\r')
        for animal in animals:
            file_writer.writerow(
                [os.path.join(path_to_the_dataset, animal).replace("\\", "/"),
                os.path.join(relative_path, animal),
                type]
            )


def create_file(file_name: str) -> None:
    """
    This function create a new csv-file (or rewrite existed) with specified by user name
    """
    with open(file_name, 'w') as file:
        file_writer = csv.writer(file, delimiter=",", lineterminator="\r")
        file_writer.writerow(["Absolute path", "Relative path", "Type"])
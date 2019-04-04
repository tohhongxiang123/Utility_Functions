import os
import shutil
from random import shuffle, randint


def backup(root_path=None, file_ext="", output_path=None, rename=False):
    '''
    :param path: which directory to back up; if None, uses current working directory
    :param file_ext: which specific file extension to back up, if "", backs up all file exts
    :param output_path: absolute path to where to save backup, if None, uses ".\output"
    :param rename: whether to rename files to a random name (will not rename directories)
    :return: None
    '''

    if root_path is None:
        root_path = os.getcwd()
    if output_path is None:
        output_path = os.path.join(root_path, "output")
    if not os.path.exists(output_path):
        os.mkdir(output_path)

    file_count = 0
    file_size = 0
    chars = list("qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890")

    print("===== START OF FILE LIST =====")
    for folder, subfolders, files in os.walk(root_path):
        if folder.startswith(output_path):  # doesnt count anything inside output dst
            continue
        for file_name in files:
            if file_name != os.path.basename(__file__) and file_name.endswith(file_ext):
                file_count += 1
                file_size += os.path.getsize(os.path.join(folder, file_name))
                print("{} - {}".format(file_count, file_name))
    print("===== END OF FILE LIST =====")
    print("File count: {}".format(file_count))
    print("File size: {} MB".format(round(file_size/10**6, 2)))
    print("Root directory to copy from: {}".format(root_path))
    print("Specific file extensions to copy: {}".format(file_ext))
    print("Output path to copy to: {}".format(output_path))
    print("Renaming files to random names: {}".format(rename))

    while True:
        answer = input("Do you want to continue? y for yes, n for no\n").lower()
        if answer not in ["y", "n"]:
            print("Invalid input: {}".format(answer))
        else:
            break

    if answer == "y":
        # copying the files
        print("Copying {} file(s) into {}".format(file_count, output_path))
        for folder, subfolders, files in os.walk(root_path):
            current_folder = os.path.relpath(folder, root_path)

            # makes sure output path and contents are not copied
            if folder.startswith(output_path):
                continue
            # make sure the directory exists in output dst before copying file into output dst
            if not os.path.exists(os.path.join(output_path, current_folder)):
                os.mkdir(os.path.join(output_path, current_folder))

            for file_name in files:
                if file_name != os.path.basename(__file__) and file_name.endswith(file_ext):
                    current_file_path = os.path.join(root_path, current_folder, file_name)
                    if rename:  # generate a random filename with extension
                        shuffle(chars)
                        base_name = "".join(chars[:randint(5, 10)])
                        current_file_ext = file_name.split(".")[-1]
                        new_file_name = base_name + "." + current_file_ext
                        new_file_path = os.path.join(output_path, current_folder, new_file_name)
                    else:
                        new_file_path = os.path.join(output_path, current_folder, file_name)

                    shutil.copy(current_file_path, new_file_path)

        for folder, _, _ in os.walk(output_path):  # removes empty directories
            if not os.listdir(folder):
                os.rmdir(folder)

        print("Done")
    else:
        print("Copying cancelled")
        quit()

if __name__ == "__main__":
    backup()


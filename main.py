# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from typing import List
import os


def get_subdir_list() -> List[str]:
    current_dir = os.getcwd()
    subdir_list = []
    for filename in os.listdir(current_dir):
        dir = os.path.join(current_dir, filename)
        if filename[0] == ".":
            continue
        if os.path.isdir(dir):
            subdir_list.append(os.path.join(current_dir, filename))
    return subdir_list


def check_file_structure(dir: str) -> bool:
    prefix = dir[-5:]
    suffixes = ["_around_images", "_lidar_data", "_surround_images", "_pegasus_images"]
    for suffix in suffixes:
        subdir = os.path.join(dir, prefix + suffix)
        if not os.path.exists(subdir):
            print("Error: ", prefix + suffix, " dont exits")
            return False
    return True

def get_size(start_path:str)->float:
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            # skip if it is symbolic link
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)

    return total_size


def remove_too_small_file(dir: str):
    threshold_bety = 1500 * 1024 * 1024
    prefix = dir[-5:]
    suffixes = ["_lidar_data"]
    lidar_data = os.path.join(dir, prefix + suffixes[0])
    delete_paths = []
    for filename in os.listdir(lidar_data):
        file_path = os.path.join(lidar_data, filename)
        if os.path.getsize(file_path) < threshold_bety:
            cmd = "rm " + file_path
            print(cmd)
            os.system(cmd)
            continue
        delete_paths.append(file_path)

        if file_path[-6:] == "active":
            target_name = file_path[:-7]
            org_active_name = target_name + ".orig.active"
            cmd = "rosbag reindex " + file_path + " && rm " + org_active_name + " && " + " mv " + file_path + " " + target_name
            print(cmd)
            os.system(cmd)

    suffixes = ["_around_images", "_surround_images", "_pegasus_images"]
    for suffix in suffixes:
        suffixe_dir=os.path.join(dir,prefix+suffix)
        for filename in os.listdir(suffixe_dir):
            file_path = os.path.join(suffixe_dir, filename)
            if get_size(file_path)<threshold_bety:
                cmd = "rm -r " + file_path
                print(cmd)
                os.system(cmd)
                continue

            # todo terminal line in system


def reference_time_stamp(dir: str, suffixes: str) -> List[str]:
    prefix = dir[-5:]
    time_stamp_reference = []
    lidar_data = os.path.join(dir, prefix + suffixes)
    for filename in os.listdir(lidar_data):
        time_stamp_reference.append(filename[:19])
    return time_stamp_reference


def remove_ioslate_msgs(dir: str):
    prefix = dir[-5:]
    suffixes = ["_around_images", "_lidar_data", "_surround_images", "_pegasus_images"]
    referece_time_stamp_list = []
    for suffix in suffixes:
        referece_time_stamp_list.append(reference_time_stamp(dir, suffix))

    for suffix in suffixes:
        subdir = os.path.join(dir, prefix + suffix)
        for filename in os.listdir(subdir):
            time_stamp = filename[:19]
            for reference_time_stamps in referece_time_stamp_list:
                if time_stamp not in reference_time_stamps:
                    filepath = os.path.join(subdir, filename)
                    cmd = "rm "
                    if os.path.isdir(filepath):
                        cmd = "rm -r "
                    cmd += filepath
                    print(cmd)
                    os.system(cmd)
                    # todo delete dir


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    subdir_listes = get_subdir_list()
    for subdir in subdir_listes:
        if not check_file_structure(subdir):
            break
        # if not check_name_system(subdir):
        #     break
        remove_too_small_file(subdir)
        remove_ioslate_msgs(subdir)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

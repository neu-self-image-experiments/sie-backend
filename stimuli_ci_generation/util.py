import shutil
import os


def clean_local_dir(directory):
    shutil.rmtree(directory)


def mkdir(participant_id, *args):
    tmp_dir = f"/tmp/{participant_id}/"
    for nested_path in args:
        tmp_dir += f"{nested_path}/"

    try:
        os.makedirs(tmp_dir, exist_ok=True)  # suppressed FileExistsError
    except OSError:
        print("Directory '%s' can not be created" % tmp_dir)

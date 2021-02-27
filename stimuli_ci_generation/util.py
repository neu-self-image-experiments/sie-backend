import shutil
import os


def mkdir(participant_id, *args):
    """
    Create directories in tmp dir
    Args:
        participant_id: participant id
        args: varargs for optional nested paths
    Returns:
        path to specified directory
    """

    tmp_dir = f"/tmp/{participant_id}/"
    for nested_path in args:
        tmp_dir += f"{nested_path}/"

    try:
        os.makedirs(tmp_dir, exist_ok=True)  # suppressed FileExistsError
    except OSError:
        print("Directory '%s' can not be created" % tmp_dir)
    
    return tmp_dir

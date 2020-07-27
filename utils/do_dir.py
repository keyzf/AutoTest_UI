import shutil
from config.PATH import *


def rmdir_next_mkdir(dir_path):
    """清空目录"""
    try:
        if os.path.exists(dir_path):
            shutil.rmtree(dir_path)
            os.mkdir(dir_path)
        else:
            os.mkdir(dir_path)
    except Exception as e:
        raise e


def copy_to_dir(source_dir, target_dir):
    """复制一个文件夹（包括文件夹本身和旗下内容）到另一个文件夹下"""
    try:
        shutil.copytree(source_dir, os.path.join(target_dir, os.path.split(source_dir)[-1]))
    except Exception as e:
        raise e

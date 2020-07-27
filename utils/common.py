import inspect
import os


def get_module_name():
    # last=inspect.stack()[1]
    module_path = inspect.stack()[1][1]
    module_file = os.path.basename(module_path)
    # moduleName = moduleFile.split(".")[0]
    # print("last is:",last)
    # print("modulePath:",modulePath)
    # print("moduleFile:", moduleFile)
    return module_file


def get_method_name():
    # print('methodName :'+inspect.stack()[1][3])
    return inspect.stack()[1][3]


# def remove_dir(dir_path):
#     if not os.path.isdir(dir_path):
#         return
#     files = os.listdir(dir_path)
#     try:
#         for file in files:
#             filePath = os.path.join(dir_path, file)
#             if os.path.isfile(filePath):
#                 os.remove(filePath)
#             elif os.path.isdir(filePath):
#                 remove_dir(filePath)
#         os.rmdir(dir_path)
#     except Exception:
#         print(Exception)


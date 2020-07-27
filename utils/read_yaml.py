import yaml
from config.PATH import *


class ReadYaml:
    def __init__(self, filepath=YAML):
        if os.path.exists(filepath):
            self.yaml = filepath
        else:
            raise FileNotFoundError('{} 不存在！！！'.format(filepath))

    def get_yaml(self):
        with open(self.yaml, 'r', encoding='UTF-8') as f:
            yaml_data = yaml.safe_load(f)
            return yaml_data


if __name__ == '__main__':
    # r = ReadYaml().get_yaml()
    # print(r["USER_INFO"])
    pass

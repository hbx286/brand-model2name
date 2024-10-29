import os
import re
import json
from typing import Dict
from git import Repo

from .brand_map import brand_map



class HandleBrandModel:

    def __init__(self, repo_path: str = None) -> None:
        self.repo_path = repo_path
        if not self.repo_path:
            current_file_dir = os.path.dirname(os.path.abspath(__file__))
            while current_file_dir:
                if os.path.isdir(os.path.join(current_file_dir, '.git')):
                    self.repo_path = current_file_dir
                    break
                current_file_dir = os.path.dirname(current_file_dir)
        self.repo = Repo(self.repo_path)
        self.sub_module = 'MobileModels'


    @property
    def last_commit_hash(self) -> str:
        directory = os.path.dirname(os.path.abspath(__file__))
        with open(f"{directory}/.last_hash", "r", encoding='utf-8') as f:
            return f.readline()


    def update_submodule(self) -> str:
        if not self.repo.submodules:
            self.repo.create_submodule(
                name=self.sub_module,
                path=self.sub_module,
                url="https://github.com/KHwang9883/MobileModels.git",
                branch="master"
            )
        sub_module = self.repo.submodule(self.sub_module)
        sub_module.update(init=True, recursive=True, force=True)
        sub_module.module().git.pull()
        return sub_module.module().head.commit.hexsha


    @staticmethod
    def process_markdown(file_path: str, brand: str) -> Dict[str, Dict[str, str]]:
        with open(file_path, 'r', encoding='utf-8') as f:
            results = {}
            for line in f.readlines():
                line = line.replace('\n', '')
                if not line or \
                    ":" not in line or \
                    line.startswith('*') or \
                    line.startswith('- ') or \
                    line.startswith('#'):
                    continue
                keys, value = line.split(':')
                value = value.strip(' ')
                for key in re.findall(r'`([^`]+)`', keys):
                    results[key] = {}
                    results[key]['brand'] = brand
                    results[key]['model'] = value
            return results


    def get_sub_module_files(self) -> Dict[str, str]:
        submodule_path = os.path.join(self.repo_path, self.sub_module, 'brands')
        results = {}
        if os.path.isdir(submodule_path):
            for file in os.listdir(submodule_path):
                file_path = os.path.join(submodule_path, file)
                if os.path.isfile(file_path):
                    results[file.split('.md')[0]] = file_path
        return results


    def finish(self) -> None:
        directory = os.path.dirname(os.path.abspath(__file__))
        with open(f"{directory}/.last_hash", "w+", encoding='utf-8') as f:
            f.write(self.repo.submodule(self.sub_module).module().head.commit.hexsha)


    def workflow(self) -> None:
        directory = f"{os.path.dirname(os.path.abspath(__file__))}/data"
        os.makedirs(directory, exist_ok=True)
        latest_commit_hash = self.update_submodule()
        if self.last_commit_hash == latest_commit_hash:
            print('No new data')
            return
        for key, value in self.get_sub_module_files().items():
            brand = brand_map.get(key, {}).get('brand', '')
            data = self.process_markdown(value, brand)
            with open(f"{directory}/{key}.json", 'w+', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        self.finish()


if __name__ == '__main__':
    HandleBrandModel().workflow()






import json
import os
from typing import List, Dict, Literal
from .brand_map import BRANDS, brand_dict, mobile, tv, wearable


class Model2Name:

    _models = {}

    def __init__(
            self,
            *,
            brands: List[str] = BRANDS,
            device: Literal['mobile', 'tv', 'wearable', 'all'] = 'mobile'
        ) -> None:
        self.brands = brands
        self.device = device


    def load_data(self) -> None:
        file_paths = set()
        if self.device == 'all':
            file_source = brand_dict
        elif self.device == 'mobile':
           file_source = mobile
        elif self.device == 'tv':
            file_source = tv
        elif self.device == 'wearable':
            file_source = wearable
        else:
            raise ValueError(f"Invalid device type: {self.device}")
        for brand in self.brands:
            file_paths.update(file_source.get(brand, []))
        directory = f"{os.path.dirname(os.path.abspath(__file__))}/data"
        for file_path in file_paths:
            with open(f'{directory}/{file_path}.json', 'r', encoding='utf-8') as f:
                self._models.update(json.load(f))


    def get_model_name(self, model: str) -> Dict:
        if not self._models:
            self.load_data()
        return self._models.get(model, {})


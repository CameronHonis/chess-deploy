import re
from typing import Dict, Any
import yaml


def to_snake_case(string: str) -> str:
    return re.sub(r'(?<!^)(?=[A-Z])', '_', string).lower()


def to_snake_keys(obj: Dict[str, Any]) -> Dict[str, Any]:
    out = {}
    for key, value in obj.items():
        if isinstance(value, dict):
            value = to_snake_keys(value)
        out[to_snake_case(key)] = value

    return out


def load_snaked_yml(path: str) -> Dict[str, Any]:
    with open(path, "r") as file:
        return to_snake_keys(yaml.safe_load(file))

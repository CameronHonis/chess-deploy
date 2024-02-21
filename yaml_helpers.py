import re
from typing import Dict, Any, List
import yaml


# def to_snake_case(string: str) -> str:
#     return re.sub(r'(?<!^)(?=[A-Z])', '_', string).lower()


def to_snake_case(camelCase: str) -> str:
    chars: List[str] = []
    lastWasUpper = False
    for i, char in enumerate(camelCase):
        no_split = len(chars) == 0 or chars[-1] == '_' or lastWasUpper
        if char.isupper() and not no_split:
            chars.append('_')
        chars.append(char.lower())
        lastWasUpper = char.isupper()
    return ''.join(chars)


def to_snake_keys(obj: Dict[str, Any]) -> Dict[str, Any]:
    out = {}
    for key, value in obj.items():
        if isinstance(value, dict):
            value = to_snake_keys(value)
        elif isinstance(value, list):
            value = [to_snake_keys(item) if isinstance(item, dict) else item for item in value]
        out[to_snake_case(key)] = value

    return out


def load_snaked_yml(path: str) -> Dict[str, Any]:
    with open(path, "r") as file:
        return to_snake_keys(yaml.safe_load(file))

def test_to_snake_case():
    assert to_snake_case("camelCase") == "camel_case"
    assert to_snake_case("CamelCase") == "camel_case"
    assert to_snake_case("CamelCASE") == "camel_case"
    assert to_snake_case("camelCASE") == "camel_case"
    assert to_snake_case("camel_case") == "camel_case"
    assert to_snake_case("Camel_Case") == "camel_case"
    assert to_snake_case("Camel_CASE") == "camel_case"
    assert to_snake_case("camel_CASE") == "camel_case"
    assert to_snake_case("camel") == "camel"
    assert to_snake_case("Camel") == "camel"
    assert to_snake_case("CAMEL") == "camel"
    assert to_snake_case("clusterIps") == "cluster_ips"
    assert to_snake_case("clusterIPs") == "cluster_ips"

if __name__ == "__main__":
    test_to_snake_case()
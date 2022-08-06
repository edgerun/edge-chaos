from dataclasses import dataclass
from typing import Dict

from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class ChaosCommand:
    name: str
    parameters: Dict
    kind: str

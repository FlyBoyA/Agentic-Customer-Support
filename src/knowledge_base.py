import json
from pathlib import Path
from typing import List, Dict


def load_knowledge_base( file_path="data/knowledge_base.json") -> List[Dict]:

    path = Path(file_path)
    if not path.exists(): raise FileNotFoundError(f"Knowledge base missing: {path}")

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
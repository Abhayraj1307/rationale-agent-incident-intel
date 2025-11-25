import os
from pathlib import Path
from typing import List, Dict


def load_incident_docs(base_dir: str = "data/incidents") -> List[Dict]:
    """
    Load all markdown incident files from the given directory.
    Returns a list of dicts: {incident_id, filename, text}.
    """
    incidents = []
    base_path = Path(base_dir)
    if not base_path.exists():
        raise FileNotFoundError(f"Incident directory not found: {base_dir}")

    for fname in os.listdir(base_dir):
        if not fname.endswith(".md"):
            continue
        path = base_path / fname
        with path.open("r", encoding="utf-8") as f:
            text = f.read()

        incident_id = fname.replace(".md", "")  # e.g. "incident_001"
        incidents.append(
            {
                "incident_id": incident_id,
                "filename": fname,
                "text": text,
            }
        )
    return incidents

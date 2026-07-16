import pandas as pd
from pathlib import Path

def ingest_ground_truth(csv_path: Path):

    """Reads the ground truth CSV and groups records by patient folder
       to ensure consistent pseudonymization across a patient's entire study."""
    if not csv_path.exists():
        raise FileNotFoundError(f"Ground truth CSV not found at {csv_path}")
    
    df = pd.read_csv(csv_path)
    return df.groupby('patient_folder')
import pandas as pd
from pathlib import Path

class SecureAuditLogger:
    def __init__(self):
        self.records = []

    def log_patient_mapping(self, pseudonym: str, orig_name: str, orig_id: str, total_images: int, hosp_code="STF", modality="US00"):

        """Formats the tracking data into an un-clustered Key:Value structure."""
        image_range = f"0001 to {total_images:04d}"
        audit_value = f"Orig Name: {orig_name} -> Orig ID: {orig_id} -> Hosp: {hosp_code} -> Modality: {modality} -> Images: {image_range}"
        
        self.records.append({
            "Digital_ID (Key)": pseudonym,
            "Value (Original Data & Image Range)": audit_value
        })

    def export_secure_log(self, output_csv_path: Path):
        """Exports the mapping file to CSV."""
        df = pd.DataFrame(self.records)
        df.to_csv(output_csv_path, index=False)
import os
from pathlib import Path
import pydicom

# Import our enterprise modules
from ground_truth_ingestor import ingest_ground_truth
from cryptographic_id_generator import generate_secure_pseudonym, format_dicom_filename
from pixel_redactor import redact_visual_phi
from metadata_scrubber import scrub_dicom_headers
from secure_audit_logger import SecureAuditLogger

# --- GLOBAL PATH CONFIGURATION ---
INPUT_DIR = Path(r"D:\Work\Synth_PHI_02\CVD\Synthetic_PHI_Dataset_02")
INPUT_CSV = INPUT_DIR / "master_phi_ground_truth.csv"

# Directory where the newly scrubbed dataset will be generated
OUTPUT_DIR = Path(r"E:\CVD\Clean_Deidentified_Dataset")

def execute_pipeline():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    logger = SecureAuditLogger()
    
    print("=== Phase 1: Ingesting Ground Truth ===")
    grouped_patients = ingest_ground_truth(INPUT_CSV)
    
    print("\n=== Phase 2 & 3: Targeted De-ID & Restructuring ===")
    for patient_folder, group in grouped_patients:
        # Generate the secure Digital ID for this patient
        digital_id = generate_secure_pseudonym()
        
        # Create a new patient folder using ONLY the digital ID
        patient_out_dir = OUTPUT_DIR / f"Patient_{digital_id}"
        patient_out_dir.mkdir(parents=True, exist_ok=True)
        
        # --- FIX 1: Add  to extract the exact string from the array ---
        orig_name = group['synthetic_name'].values
        orig_id = group['synthetic_id'].values
        
        print(f"Processing Folder: {patient_folder} -> Assigned Digital ID: {digital_id}")
        
        image_counter = 1
        for index, row in group.iterrows():
            
            # --- FIX 2: Dynamically reconstruct the path to avoid mismatch ---
            dcm_filename = Path(row['new_dcm_path']).name
            dcm_path = INPUT_DIR / patient_folder / dcm_filename
            
            if not dcm_path.exists():
                print(f"  ⚠️ File not found, skipping: {dcm_path}")
                continue
                
            try:
                # 1. Read the synthetic DICOM file
                ds = pydicom.dcmread(str(dcm_path), force=True)
                
                # 2. Redact the burned-in pixels
                ds = redact_visual_phi(ds, row['bounding_box'])
                
                # 3. Scrub the metadata headers
                ds = scrub_dicom_headers(ds, digital_id)
                
                # 4. Generate the 16-character filename and save
                new_filename = format_dicom_filename(digital_id, image_counter)
                new_dcm_path = patient_out_dir / new_filename
                ds.save_as(str(new_dcm_path))
                
                image_counter += 1
                
            except Exception as e:
                print(f"  ⚠️ Error processing {dcm_filename}: {e}")
                
        # Log this patient's successful mapping to the audit trail
        if image_counter > 1:
            logger.log_patient_mapping(digital_id, orig_name, orig_id, image_counter - 1)

    print("\n=== Phase 4: Exporting Secret Master Audit Log ===")
    audit_csv_path = OUTPUT_DIR / "master_file_GT.csv"
    logger.export_secure_log(audit_csv_path)
    
    print(f"✅ Secure Audit Log generated at: {audit_csv_path}")
    print(f"🎉 Pipeline exe Complete! \n Clean dataset located in: {OUTPUT_DIR}")

if __name__ == "__main__":
    execute_pipeline()
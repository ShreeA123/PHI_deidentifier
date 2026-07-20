# 🚀 DICOM De-Identification & Pseudonymization Pipeline
This project provides a modular pipeline designed to securely de-identify and pseudonymize Protected Health Information (PHI) from medical imaging datasets.
Medical images suffer from the "iceberg problem," where sensitive identifiers are visible in the image pixels and hidden within the DICOM structural metadata.
This pipeline acts as an automated rescue mission. It systematically scrubs the dataset to satisfy the Health Insurance Portability and Accountability Act (HIPAA) Privacy Rule's Safe Harbor method.
By utilizing mathematically perfect bounding box coordinates from a previously established ground truth, this system precisely masks visual PHI and implements a highly secure 16-character alphanumeric pseudonymization system for safe AI research and validation.

## 📦 Table of Contents
- Architecture & Modules
- The 16-Character Digital ID System
- Dataset Overview
- Tech Stack
- Installation & Setup
- Usage
- Understanding HIPAA Safe Harbor & Audit Logging

## 🛠 Architecture & Modules
To ensure scalability and maintainability, this project utilizes a modular architecture rather than a single monolithic script.

- `ground_truth_ingestor.py`: Ingests the master_phi_ground_truth.csv and groups records by patient folder to - ensure consistent pseudonymization across a patient's entire study.

- `cryptographic_id_generator.py`: The Identity Engine. Under the HIPAA Safe Harbor method for re-identification, a re-identification code must not be derived from or related to information about the individual. This module generates a cryptographically secure random alphanumeric string to comply with this requirement.

- `pixel_redactor.py`: The Visual Module. Uses the exact bounding box coordinates from the ground truth to apply a mathematically perfect black mask over the burned-in text, permanently obscuring visual PHI.

- `metadata_scrubber.py`: The Medical Scrubber. Scrubs the DICOM headers of explicit identifiers like Patient's Name, Patient ID, and Birth Date. It then injects the new Digital ID to maintain DICOM validity.

- `secure_audit_logger.py`: The Audit Trail. Formats the tracking data into a highly confidential Key:Value mapping structure (pairing the new ID with the original identity and image range) and exports it as `master_file_GT.csv`.

- `deid_pipeline_orchestrator.py`: The Master Orchestrator. The main executable that imports the modules above, maps absolute paths dynamically, and orchestrates the end-to-end execution.

## The 16-Character Digital ID System
To maintain organized, traceable data while replacing direct identifiers, this pipeline utilizes pseudonymization. Every processed file is renamed using a strict 16-character nomenclature: [HOS]-[PATID]-[MODL]-[IMG#].
- HOS (3 letters): Hospital/Site Code (e.g., STF for Stanford).
- PATID (5 chars): A randomly generated, cryptographically secure alphanumeric pseudonym for the patient (e.g., A9K3P).
- MODL (4 chars): Modality/Technique (e.g., US00 for Ultrasound).
- IMG# (4 digits): Sequential image number (e.g., 0001).
Example Output: STF-A9K3P-US00-0001.dcm

## Dataset Overview
- Source: Stanford Lung Database (OpenPOCUS).
- Scope: Images derived from a multi-center study involving 226 adult patients presenting to emergency departments with respiratory symptoms.
- Format: Ultrasound images encapsulated in the Digital Imaging and Communications in Medicine (DICOM) standard format.

## Tech Stack
- Language: Python
- Environment/IDE: VS Code
- Data Processing & Array Manipulation: pandas and numpy
- Medical Imaging / DICOM Parsing: pydicom library

## Installation & Setup
It is recommended to run this pipeline within a virtual environment to prevent dependency conflicts with your system's global Python installation.

Create and activate a virtual environment: 
###  Windows
- python -m venv enterprise_deid
- .\enterprise_deid\Scripts\activate

### Mac/Linux
- python3 -m venv enterprise_deid
- source enterprise_deid/bin/activate

Install dependencies using the provided requirements.txt file:
`pip install -r requirements.txt`

## Usage
1. Open `deid_pipeline_orchestrator.py` in your text editor.
2. Update the Global Path Configurations at the top of the file to point to your local directories:
- INPUT_DIR: The dataset folder containing the previously generated synthetic data and the `master_phi_ground_truth.csv`.
- OUTPUT_DIR: The destination folder for the cleaned .dcm files and the secret audit log.
3. Execute the pipeline:
`python deid_pipeline_orchestrator.py`

## Understanding HIPAA Safe Harbor & Audit Logging
Digital Imaging and Communications in Medicine (DICOM) is the global technical standard for the digital storage and transmission of medical images. A .dcm file securely groups pixel data together with a highly structured list of metadata attributes. To comply with the HIPAA Privacy Rule's Safe Harbor method, 18 specific categories of identifiers must be removed or sanitized from these headers.
Pseudonymization reduces direct identifiability, but the data can still be re-linked to a person if you have a separate mapping key. To support secure research and authorized re-identification, the secure_audit_logger.py module generates a master_file_GT.csv audit log. This highly confidential file pairs the new 16-character Digital IDs with the original patient data in an unclustered Key:Value format. Access to this file must be strictly limited to authorized personnel to maintain compliance.

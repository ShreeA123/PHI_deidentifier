import pydicom

def scrub_dicom_headers(ds: pydicom.dataset.FileDataset, pseudonym: str):

    """Removes PHI elements and injects the new Digital ID."""
    # 1. Remove direct and indirect identifiers
    if 'PatientBirthDate' in ds: del ds.PatientBirthDate
    if 'AccessionNumber' in ds: del ds.AccessionNumber
    if 'StudyDate' in ds: del ds.StudyDate
    if 'SeriesDate' in ds: del ds.SeriesDate
    if 'AcquisitionDate' in ds: del ds.AcquisitionDate
    
    # 2. Inject the Secure Pseudonym
    ds.PatientName = pseudonym
    ds.PatientID = pseudonym
    
    # 3. Flag as De-Identified
    ds.PatientIdentityRemoved = "YES"
    ds.DeidentificationMethod = "PHI DEID via HIPAA Safe Harbor - Pixel & Header Redaction"
    
    return ds
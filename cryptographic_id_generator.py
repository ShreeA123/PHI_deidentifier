import string
import secrets

def generate_secure_pseudonym(length=5):

    """Generates a cryptographically secure random alphanumeric string of specified length"""

    alphabet = string.ascii_uppercase + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def format_dicom_filename(pseudonym: str, counter: int, hosp_code="STF", modality="US00"):

    """Enforces the 16-character nomenclature rule: [HOS]-[PATID]-[MODL]-[IMG#] """
    
    return f"{hosp_code}-{pseudonym}-{modality}-{counter:04d}.dcm"

import ast
import pydicom

def redact_visual_phi(ds: pydicom.dataset.FileDataset, bbox_str: str):
   
    """Reads the bounding box coordinates and overwrites the specified
    pixel region with black to permanently obscure burned-in PHI."""
    # Convert string representation of tuple back to actual tuple
    bbox = ast.literal_eval(bbox_str)
    x1, y1, x2, y2 = [int(coord) for coord in bbox]
    
    pixel_array = ds.pixel_array
    # Apply a black mask over the region
    pixel_array[y1:y2, x1:x2] = 0  
    
    # Update the DICOM pixel data
    ds.PixelData = pixel_array.tobytes()
    return ds
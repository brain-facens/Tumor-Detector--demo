# imports
from pathlib import Path

import nibabel as nib
import numpy as np


def load_nii(file_path: Path) -> np.ndarray:
    nii_file = nib.load(filename=file_path)
    content = np.asanyarray(a=nii_file.dataobj)
    return content

def load_predict(file_path: Path) -> np.ndarray:
    with open(file=file_path, mode='rb') as np_file:
        content = np.load(file=np_file)['data']
        return content

def apply_mask_theshold(mask: np.ndarray, threshold: float) -> np.ndarray:
    th_mask = (mask >= threshold).astype(dtype=np.float32)
    return th_mask

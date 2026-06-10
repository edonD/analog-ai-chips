"""SpiceGlass — open SpiceVision for the AI design era (M0)."""
from .classify import classify_design
from .db import Design, Device, Subckt
from .parser import parse_file, parse_text

__version__ = "0.1.0"


def load(path: str) -> Design:
    design = parse_file(path)
    classify_design(design)
    return design

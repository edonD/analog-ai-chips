"""SpiceGlass — open SpiceVision for the AI design era (M0)."""
from .engine.classify import classify_design
from .engine.db import Design, Device, Subckt
from .engine.parser import parse_file, parse_text

__version__ = "0.1.0"


def load(path: str) -> Design:
    design = parse_file(path)
    classify_design(design)
    return design

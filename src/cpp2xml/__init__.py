"""cpp2xml - Parse C++ headers and generate XML documentation."""

__version__ = "0.1.0"

from .parser import CppParser
from .xml_generator import XmlGenerator

__all__ = ["CppParser", "XmlGenerator"]

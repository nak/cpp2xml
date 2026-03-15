"""Tests for the XML generator."""

import unittest
from pathlib import Path
import sys
import tempfile
import shutil
import xml.etree.ElementTree as ET

# Add src to path for testing
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from cpp2xml.parser import CppParser
from cpp2xml.xml_generator import XmlGenerator


class TestXmlGenerator(unittest.TestCase):
    """Test cases for XmlGenerator."""

    @classmethod
    def setUpClass(cls):
        """Set up test fixtures."""
        cls.fixtures_dir = Path(__file__).parent / "fixtures" / "include"
        cls.parser = CppParser(include_paths={str(cls.fixtures_dir): 'test_generator_pkg'})

    def setUp(self):
        """Set up test output directory."""
        self.output_dir = tempfile.mkdtemp()
        self.generator = XmlGenerator(output_dir=self.output_dir)

    def tearDown(self):
        """Clean up test output directory."""
        shutil.rmtree(self.output_dir)

    def test_generate_xml_for_functions(self):
        """Test XML generation for functions."""
        header_path = self.fixtures_dir / "simple.h"
        result = self.parser.parse_header(str(header_path))

        xml_content = self.generator.generate_xml(result)
        self.assertIn("<header", xml_content)
        self.assertIn("<functions>", xml_content)
        self.assertIn("<function", xml_content)
        self.assertIn('name="add"', xml_content)
        print(xml_content)

    def test_generate_xml_for_classes(self):
        """Test XML generation for classes."""
        header_path = self.fixtures_dir / "classes.h"
        result = self.parser.parse_header(str(header_path))

        xml_content = self.generator.generate_xml(result)
        self.assertIn("<classes>", xml_content)
        self.assertIn("<class", xml_content)
        self.assertIn('name="Derived"', xml_content)
        self.assertIn("<base_classes>", xml_content)
        self.assertIn("<methods>", xml_content)

    def test_generate_xml_for_structs(self):
        """Test XML generation for structs."""
        header_path = self.fixtures_dir / "structs.h"
        result = self.parser.parse_header(str(header_path))

        xml_content = self.generator.generate_xml(result)
        self.assertIn("<structs>", xml_content)
        self.assertIn("<struct", xml_content)
        self.assertIn('name="Point"', xml_content)
        self.assertIn("<fields>", xml_content)

    def test_generate_xml_for_templates(self):
        """Test XML generation for templates."""
        header_path = self.fixtures_dir / "templates.h"
        result = self.parser.parse_header(str(header_path))

        xml_content = self.generator.generate_xml(result)
        self.assertIn("<templates>", xml_content)
        self.assertIn("<template", xml_content)

    def test_anonymous_parameters_in_xml(self):
        """Test that anonymous parameters are properly represented in XML."""
        header_path = self.fixtures_dir / "simple.h"
        result = self.parser.parse_header(str(header_path))

        xml_content = self.generator.generate_xml(result)
        self.assertIn('is_anonymous="true"', xml_content)
        self.assertIn('anonymous_id=', xml_content)
        self.assertIn("<type_definition", xml_content)

    def test_write_xml_creates_file(self):
        """Test that write_xml creates the output file."""
        header_path = self.fixtures_dir / "simple.h"
        result = self.parser.parse_header(str(header_path))
        self.generator.write_xml('test_generator_pkg', result)
        output_file = Path(self.output_dir) / 'test_generator_pkg' / "simple.xml"
        self.assertTrue(output_file.exists())

    def test_output_directory_structure(self):
        """Test that output directory structure mirrors source."""
        header_path = self.fixtures_dir / "subdir" / "nested.h"
        result = self.parser.parse_header(str(header_path))

        self.generator.write_xml('test_generator_pkg', result)

        output_file = Path(self.output_dir) / 'test_generator_pkg' / "subdir" / "nested.xml"
        self.assertTrue(output_file.exists())

    def test_xml_is_valid(self):
        """Test that generated XML is valid."""
        header_path = self.fixtures_dir / "simple.h"
        result = self.parser.parse_header(str(header_path))

        self.generator.write_xml('test_generator_pkg', result)
        output_file = Path(self.output_dir) / 'test_generator_pkg' /"simple.xml"

        # Try to parse the XML
        tree = ET.parse(output_file)
        root = tree.getroot()

        self.assertEqual(root.tag, "header")
        self.assertIsNotNone(root.get("file"))

    def test_generate_all(self):
        """Test generating XML for all parsed headers."""
        results = self.parser.parse_all_headers()
        self.generator.generate_all(results)

        # Check that XML files were created
        xml_files = list(Path(self.output_dir).rglob("*.xml"))
        self.assertGreater(len(xml_files), 0)

    def test_namespace_in_xml(self):
        """Test that namespace information is included in XML."""
        header_path = self.fixtures_dir / "namespaces.h"
        result = self.parser.parse_header(str(header_path))

        xml_content = self.generator.generate_xml(result)

        # Check that namespace attribute appears in XML
        if any(f.namespace for f in result.functions):
            self.assertIn('namespace=', xml_content)

        # Check specific namespaces
        if any(f.namespace == "outer" for f in result.functions):
            self.assertIn('namespace="outer"', xml_content)

        if any(f.namespace == "outer::inner" for f in result.functions):
            self.assertIn('namespace="outer::inner"', xml_content)
        print(xml_content)


if __name__ == "__main__":
    unittest.main()

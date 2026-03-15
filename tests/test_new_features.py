"""Tests for newly added C++ features."""

import unittest
from pathlib import Path
import sys

# Add src to path for testing
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from cpp2xml.parser import CppParser
from cpp2xml.xml_generator import XmlGenerator


class TestEnums(unittest.TestCase):
    """Test cases for enum parsing."""

    @classmethod
    def setUpClass(cls):
        """Set up test fixtures."""
        cls.fixtures_dir = Path(__file__).parent / "fixtures" / "include"
        cls.parser = CppParser(include_paths=[str(cls.fixtures_dir)])

    def test_parse_enums(self):
        """Test parsing regular enums."""
        header_path = self.fixtures_dir / "enums.h"
        result = self.parser.parse_header(str(header_path))

        self.assertGreater(len(result.enums), 0)

        # Find Color enum
        color_enums = [e for e in result.enums if e.name == "Color"]
        self.assertGreater(len(color_enums), 0)
        color = color_enums[0]
        self.assertFalse(color.is_scoped)
        self.assertEqual(len(color.values), 3)
        self.assertIn("RED", [v.name for v in color.values])

    def test_parse_enum_class(self):
        """Test parsing scoped enums (enum class)."""
        header_path = self.fixtures_dir / "enums.h"
        result = self.parser.parse_header(str(header_path))

        # Find Direction enum class
        direction_enums = [e for e in result.enums if e.name == "Direction"]
        if direction_enums:
            direction = direction_enums[0]
            self.assertTrue(direction.is_scoped)
            self.assertEqual(len(direction.values), 4)

    def test_enum_with_values(self):
        """Test parsing enums with explicit values."""
        header_path = self.fixtures_dir / "enums.h"
        result = self.parser.parse_header(str(header_path))

        # Find StatusCode enum
        status_enums = [e for e in result.enums if e.name == "StatusCode"]
        if status_enums:
            status = status_enums[0]
            # Values should be captured
            self.assertGreater(len(status.values), 0)


class TestUnions(unittest.TestCase):
    """Test cases for union parsing."""

    @classmethod
    def setUpClass(cls):
        """Set up test fixtures."""
        cls.fixtures_dir = Path(__file__).parent / "fixtures" / "include"
        cls.parser = CppParser(include_paths=[str(cls.fixtures_dir)])

    def test_parse_unions(self):
        """Test parsing union declarations."""
        header_path = self.fixtures_dir / "unions.h"
        result = self.parser.parse_header(str(header_path))

        self.assertGreater(len(result.unions), 0)

        # Find Data union
        data_unions = [u for u in result.unions if u.name == "Data"]
        self.assertGreater(len(data_unions), 0)
        data = data_unions[0]
        self.assertEqual(len(data.fields), 3)

    def test_union_with_methods(self):
        """Test parsing unions with methods."""
        header_path = self.fixtures_dir / "unions.h"
        result = self.parser.parse_header(str(header_path))

        # Find Value union
        value_unions = [u for u in result.unions if u.name == "Value"]
        if value_unions:
            value = value_unions[0]
            self.assertGreater(len(value.methods), 0)


class TestOperators(unittest.TestCase):
    """Test cases for operator overload parsing."""

    @classmethod
    def setUpClass(cls):
        """Set up test fixtures."""
        cls.fixtures_dir = Path(__file__).parent / "fixtures" / "include"
        cls.parser = CppParser(include_paths=[str(cls.fixtures_dir)])

    def test_parse_member_operators(self):
        """Test parsing member operator overloads."""
        header_path = self.fixtures_dir / "operators.h"
        result = self.parser.parse_header(str(header_path))

        # Find Complex class
        complex_classes = [c for c in result.classes if c.name == "Complex"]
        self.assertGreater(len(complex_classes), 0)
        complex_cls = complex_classes[0]

        # Should have operator overloads
        self.assertGreater(len(complex_cls.operators), 0)

        # Check for specific operators
        op_kinds = [op.operator_kind for op in complex_cls.operators]
        self.assertIn("+", op_kinds)
        self.assertIn("==", op_kinds)

    def test_parse_free_operators(self):
        """Test parsing free function operator overloads."""
        header_path = self.fixtures_dir / "operators.h"
        result = self.parser.parse_header(str(header_path))

        # Should have free function operators
        # The operator/ declared outside the class
        if result.operators:
            op_kinds = [op.operator_kind for op in result.operators]
            self.assertIn("/", op_kinds)


class TestVariadicTemplates(unittest.TestCase):
    """Test cases for variadic template parsing."""

    @classmethod
    def setUpClass(cls):
        """Set up test fixtures."""
        cls.fixtures_dir = Path(__file__).parent / "fixtures" / "include"
        cls.parser = CppParser(include_paths=[str(cls.fixtures_dir)])

    def test_parse_variadic_templates(self):
        """Test parsing variadic templates."""
        header_path = self.fixtures_dir / "variadic.h"
        result = self.parser.parse_header(str(header_path))

        self.assertGreater(len(result.templates), 0)

        # Find Tuple template
        tuple_templates = [t for t in result.templates if t.name == "Tuple"]
        if tuple_templates:
            tuple_t = tuple_templates[0]
            self.assertTrue(tuple_t.is_variadic)


class TestNestedTypes(unittest.TestCase):
    """Test cases for nested type parsing."""

    @classmethod
    def setUpClass(cls):
        """Set up test fixtures."""
        cls.fixtures_dir = Path(__file__).parent / "fixtures" / "include"
        cls.parser = CppParser(include_paths=[str(cls.fixtures_dir)])

    def test_parse_nested_classes(self):
        """Test parsing nested classes."""
        header_path = self.fixtures_dir / "nested.h"
        result = self.parser.parse_header(str(header_path))

        # Find Outer class
        outer_classes = [c for c in result.classes if c.name == "Outer"]
        self.assertGreater(len(outer_classes), 0)
        outer = outer_classes[0]

        # Should have nested classes
        self.assertGreater(len(outer.nested_classes), 0)

        # Check for Inner class
        self.assertIn("Inner", [nc.name for nc in outer.nested_classes])

    def test_parse_nested_structs(self):
        """Test parsing nested structs."""
        header_path = self.fixtures_dir / "nested.h"
        result = self.parser.parse_header(str(header_path))

        outer_classes = [c for c in result.classes if c.name == "Outer"]
        if outer_classes:
            outer = outer_classes[0]
            self.assertGreater(len(outer.nested_structs), 0)
            self.assertIn("Config", [ns.name for ns in outer.nested_structs])

    def test_parse_nested_enums(self):
        """Test parsing nested enums."""
        header_path = self.fixtures_dir / "nested.h"
        result = self.parser.parse_header(str(header_path))

        outer_classes = [c for c in result.classes if c.name == "Outer"]
        if outer_classes:
            outer = outer_classes[0]
            self.assertGreater(len(outer.nested_enums), 0)
            self.assertIn("Status", [ne.name for ne in outer.nested_enums])


class TestFriends(unittest.TestCase):
    """Test cases for friend declaration parsing."""

    @classmethod
    def setUpClass(cls):
        """Set up test fixtures."""
        cls.fixtures_dir = Path(__file__).parent / "fixtures" / "include"
        cls.parser = CppParser(include_paths=[str(cls.fixtures_dir)])

    def test_parse_friend_declarations(self):
        """Test parsing friend declarations."""
        header_path = self.fixtures_dir / "friends.h"
        result = self.parser.parse_header(str(header_path))

        # Find Container class
        container_classes = [c for c in result.classes if c.name == "Container"]
        if container_classes:
            container = container_classes[0]
            # Should have friend declarations
            self.assertGreater(len(container.friends), 0)


class TestDefaultParameters(unittest.TestCase):
    """Test cases for default parameter parsing."""

    @classmethod
    def setUpClass(cls):
        """Set up test fixtures."""
        cls.fixtures_dir = Path(__file__).parent / "fixtures" / "include"
        cls.parser = CppParser(include_paths=[str(cls.fixtures_dir)])

    def test_parse_default_parameters(self):
        """Test parsing functions with default parameters."""
        header_path = self.fixtures_dir / "defaults.h"
        result = self.parser.parse_header(str(header_path))

        # Find configure function
        configure_funcs = [f for f in result.functions if f.name == "configure"]
        if configure_funcs:
            configure = configure_funcs[0]
            # Should have parameters with defaults
            for param in configure.parameters:
                if param.name == "port":
                    self.assertIsNotNone(param.default_value)
                    self.assertIn("8080", param.default_value)


class TestXMLGenerationNewFeatures(unittest.TestCase):
    """Test XML generation for new features."""

    @classmethod
    def setUpClass(cls):
        """Set up test fixtures."""
        cls.fixtures_dir = Path(__file__).parent / "fixtures" / "include"
        cls.parser = CppParser(include_paths=[str(cls.fixtures_dir)])
        cls.generator = XmlGenerator(output_dir="/tmp/test_xml")

    def test_enum_xml_generation(self):
        """Test XML generation for enums."""
        header_path = self.fixtures_dir / "enums.h"
        result = self.parser.parse_header(str(header_path))

        xml_content = self.generator.generate_xml(result)
        self.assertIn("<enums>", xml_content)
        self.assertIn("<enum", xml_content)

    def test_enum_class_xml_generation(self):
        """Test XML generation for enum classes."""
        header_path = self.fixtures_dir / "enums.h"
        result = self.parser.parse_header(str(header_path))

        xml_content = self.generator.generate_xml(result)
        self.assertIn("<enum_class", xml_content)

    def test_union_xml_generation(self):
        """Test XML generation for unions."""
        header_path = self.fixtures_dir / "unions.h"
        result = self.parser.parse_header(str(header_path))

        xml_content = self.generator.generate_xml(result)
        self.assertIn("<unions>", xml_content)
        self.assertIn("<union", xml_content)

    def test_operator_xml_generation(self):
        """Test XML generation for operators."""
        header_path = self.fixtures_dir / "operators.h"
        result = self.parser.parse_header(str(header_path))

        xml_content = self.generator.generate_xml(result)
        # Member operators should be in the class
        self.assertIn("<operators>", xml_content)
        self.assertIn("<operator", xml_content)

    def test_variadic_xml_generation(self):
        """Test XML generation for variadic templates."""
        header_path = self.fixtures_dir / "variadic.h"
        result = self.parser.parse_header(str(header_path))

        xml_content = self.generator.generate_xml(result)
        self.assertIn('variadic="true"', xml_content)

    def test_nested_xml_generation(self):
        """Test XML generation for nested types."""
        header_path = self.fixtures_dir / "nested.h"
        result = self.parser.parse_header(str(header_path))

        xml_content = self.generator.generate_xml(result)
        self.assertIn("<nested_classes>", xml_content)
        self.assertIn("<nested_structs>", xml_content)
        self.assertIn("<nested_enums>", xml_content)

    def test_friend_xml_generation(self):
        """Test XML generation for friend declarations."""
        header_path = self.fixtures_dir / "friends.h"
        result = self.parser.parse_header(str(header_path))

        xml_content = self.generator.generate_xml(result)
        self.assertIn("<friends>", xml_content)
        self.assertIn("<friend", xml_content)

    def test_default_param_xml_generation(self):
        """Test XML generation for default parameters."""
        header_path = self.fixtures_dir / "defaults.h"
        result = self.parser.parse_header(str(header_path))

        xml_content = self.generator.generate_xml(result)
        self.assertIn('default=', xml_content)


if __name__ == "__main__":
    unittest.main()

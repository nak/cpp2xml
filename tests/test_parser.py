"""Tests for the C++ parser."""

import unittest
from pathlib import Path
import sys

# Add src to path for testing
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from cpp2xml.parser import CppParser


class TestCppParser(unittest.TestCase):
    """Test cases for CppParser."""

    @classmethod
    def setUpClass(cls):
        """Set up test fixtures."""
        cls.fixtures_dir = Path(__file__).parent / "fixtures" / "include"
        cls.parser = CppParser(include_paths=[str(cls.fixtures_dir)])

    def test_parse_simple_functions(self):
        """Test parsing simple functions."""
        header_path = self.fixtures_dir / "simple.h"
        result = self.parser.parse_header(str(header_path))

        self.assertEqual(len(result.functions), 3)

        # Check function names
        func_names = [f.name for f in result.functions]
        self.assertIn("add", func_names)
        self.assertIn("process", func_names)
        self.assertIn("getString", func_names)

        # Check 'add' function
        add_func = next(f for f in result.functions if f.name == "add")
        self.assertEqual(add_func.return_type, "int")
        self.assertEqual(len(add_func.parameters), 2)
        self.assertEqual(add_func.parameters[0].name, "a")
        self.assertEqual(add_func.parameters[1].name, "b")
        self.assertFalse(add_func.parameters[0].is_anonymous)

    def test_parse_anonymous_parameters(self):
        """Test parsing functions with anonymous parameters."""
        header_path = self.fixtures_dir / "simple.h"
        result = self.parser.parse_header(str(header_path))

        # Check 'process' function with anonymous params
        process_func = next(f for f in result.functions if f.name == "process")
        self.assertEqual(len(process_func.parameters), 2)
        self.assertTrue(process_func.parameters[0].is_anonymous)
        self.assertTrue(process_func.parameters[1].is_anonymous)
        self.assertIsNotNone(process_func.parameters[0].anonymous_id)
        self.assertIsNotNone(process_func.parameters[1].anonymous_id)

    def test_parse_classes(self):
        """Test parsing class declarations."""
        header_path = self.fixtures_dir / "classes.h"
        result = self.parser.parse_header(str(header_path))

        self.assertEqual(len(result.classes), 2)

        # Check Derived class
        derived = next(c for c in result.classes if c.name == "Derived")
        self.assertEqual(len(derived.base_classes), 1)
        self.assertIn("Base", derived.base_classes[0])

        # Check methods
        method_names = [m.name for m in derived.methods]
        self.assertIn("doSomething", method_names)
        self.assertIn("getValue", method_names)
        self.assertIn("setValue", method_names)

        # Check const method
        get_value = next(m for m in derived.methods if m.name == "getValue")
        self.assertTrue(get_value.is_const)

        # Check static method
        get_count = next(m for m in derived.methods if m.name == "getCount")
        self.assertTrue(get_count.is_static)

    def test_parse_structs(self):
        """Test parsing struct declarations."""
        header_path = self.fixtures_dir / "structs.h"
        result = self.parser.parse_header(str(header_path))

        self.assertEqual(len(result.structs), 2)

        # Check Point struct
        point = next(s for s in result.structs if s.name == "Point")
        self.assertEqual(len(point.fields), 3)
        field_names = [f.name for f in point.fields]
        self.assertIn("x", field_names)
        self.assertIn("y", field_names)
        self.assertIn("z", field_names)

        # Check Vector struct with methods
        vector = next(s for s in result.structs if s.name == "Vector")
        self.assertEqual(len(vector.fields), 3)
        self.assertEqual(len(vector.methods), 2)

    def test_parse_templates(self):
        """Test parsing template declarations."""
        header_path = self.fixtures_dir / "templates.h"
        result = self.parser.parse_header(str(header_path))

        self.assertGreater(len(result.templates), 0)

        # Check template class
        container_templates = [t for t in result.templates if t.name == "Container"]
        self.assertGreater(len(container_templates), 0)
        container = container_templates[0]
        self.assertEqual(container.kind, "class")
        self.assertEqual(len(container.template_parameters), 1)

        # Check template function
        max_templates = [t for t in result.templates if t.name == "max"]
        if max_templates:
            max_template = max_templates[0]
            self.assertEqual(max_template.kind, "function")
            self.assertIsNotNone(max_template.return_type)

    def test_relative_path_resolution(self):
        """Test that relative paths are correctly resolved."""
        header_path = self.fixtures_dir / "simple.h"
        result = self.parser.parse_header(str(header_path))

        self.assertEqual(result.relative_path, "simple.h")

        # Test nested path
        nested_path = self.fixtures_dir / "subdir" / "nested.h"
        result = self.parser.parse_header(str(nested_path))
        self.assertEqual(result.relative_path, "subdir/nested.h")

    def test_parse_all_headers(self):
        """Test parsing all headers in include paths."""
        results = self.parser.parse_all_headers()

        # Should find all header files
        self.assertGreater(len(results), 0)

        # Check that we got the expected headers
        relative_paths = [r.relative_path for r in results]
        self.assertIn("simple.h", relative_paths)
        self.assertIn("classes.h", relative_paths)

    def test_parse_namespaces(self):
        """Test parsing namespace information."""
        header_path = self.fixtures_dir / "namespaces.h"
        result = self.parser.parse_header(str(header_path))

        # Check outer namespace function
        outer_funcs = [f for f in result.functions if f.name == "outerFunction"]
        if outer_funcs:
            self.assertEqual(outer_funcs[0].namespace, "outer")

        # Check inner namespace function
        inner_funcs = [f for f in result.functions if f.name == "innerFunction"]
        if inner_funcs:
            self.assertEqual(inner_funcs[0].namespace, "outer::inner")

        # Check global function (no namespace)
        global_funcs = [f for f in result.functions if f.name == "globalFunction"]
        if global_funcs:
            self.assertIsNone(global_funcs[0].namespace)

        # Check classes with namespaces
        outer_classes = [c for c in result.classes if c.name == "OuterClass"]
        if outer_classes:
            self.assertEqual(outer_classes[0].namespace, "outer")

        inner_classes = [c for c in result.classes if c.name == "InnerClass"]
        if inner_classes:
            self.assertEqual(inner_classes[0].namespace, "outer::inner")

        global_classes = [c for c in result.classes if c.name == "GlobalClass"]
        if global_classes:
            self.assertIsNone(global_classes[0].namespace)


if __name__ == "__main__":
    unittest.main()
